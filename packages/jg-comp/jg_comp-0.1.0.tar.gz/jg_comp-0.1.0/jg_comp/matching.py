# jg_comp/matching.py
import collections
from .compression_strategy import CompressionStrategy

class DictionaryMatcher(CompressionStrategy):
    """Concrete compression strategy using dictionary-based matching."""

    def __init__(self, min_match_length: int = 3):
        self.min_match_length = min_match_length

    def compress(self, data: bytes) -> list:
        compressed = []
        i = 0
        max_window_size = min(1024, len(data))
        pattern_dict = collections.defaultdict(list)

        while i < len(data):
            best_match_offset, best_match_length = self._find_best_match(data, i, max_window_size, pattern_dict)

            if best_match_length >= self.min_match_length:
                if best_match_offset < i and best_match_offset <= max_window_size:
                    encoded = self._encode_match(best_match_offset, best_match_length)
                    compressed.append(encoded)
                else:
                    compressed.append(data[i])
                i += best_match_length
            else:
                compressed.append(data[i])
                i += 1

            self._update_pattern_dict(pattern_dict, data, i, max_window_size)

        return compressed

    def decompress(self, compressed_data: list) -> bytes:
        result = []
        i = 0

        while i < len(compressed_data):
            encoded = compressed_data[i]
            if isinstance(encoded, int) and encoded >= 32768:
                offset, length = self._decode_match(encoded)
                start = len(result) - offset
                result.extend(result[start:start + length])
            else:
                result.append(encoded)
            i += 1

        return bytes(result)

    def _find_best_match(self, data, current_index, max_window_size, pattern_dict):
        best_match_length = 0
        best_match_offset = 0
        window_start = max(0, current_index - max_window_size)

        for length in range(self.min_match_length, len(data) - current_index):
            current_pattern = tuple(data[current_index:current_index + length])
            if current_pattern in pattern_dict:
                for start_index in pattern_dict[current_pattern]:
                    if window_start <= start_index < current_index:
                        offset = current_index - start_index
                        if length > best_match_length:
                            best_match_length = length
                            best_match_offset = offset
            else:
                break

        return best_match_offset, best_match_length

    def _encode_match(self, offset: int, length: int) -> int:
        if offset < 128 and length < 8:
            return (1 << 15) | (offset << 8) | ((length - self.min_match_length) << 5)
        else:
            return (1 << 15) | (offset << 5) | (length - self.min_match_length)

    def _decode_match(self, encoded: int) -> tuple:
        if encoded & 0x4000:
            offset = (encoded >> 8) & 0x7F
            length = ((encoded >> 5) & 0x7) + self.min_match_length
        else:
            offset = (encoded >> 5) & 0x3FF
            length = (encoded & 0x1F) + self.min_match_length
        return offset, length

    def _update_pattern_dict(self, pattern_dict, data, current_index, max_window_size):
        for j in range(max(0, current_index - max_window_size), current_index):
            pattern = tuple(data[j:j+2])
            pattern_dict[pattern].append(j)
