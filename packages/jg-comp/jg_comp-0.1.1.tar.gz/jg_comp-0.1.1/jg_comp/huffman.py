# jg_comp/huffman.py
import heapq
import collections
import struct

class HuffmanEncoder:
    """Huffman encoder and decoder."""

    def huffman_encode(self, data: list) -> tuple:
        freq = collections.Counter(data)
        heap = [[weight, [symbol, ""]] for symbol, weight in freq.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])

        huffman_dict = {element[0]: element[1] for element in heap[0][1:]}
        encoded = ''.join(huffman_dict[byte] for byte in data)
        padding = 8 - len(encoded) % 8
        encoded += '0' * padding
        encoded_bytes = int(encoded, 2).to_bytes((len(encoded) + 7) // 8, byteorder='big')
        return struct.pack('>B', padding) + encoded_bytes, huffman_dict

    def huffman_decode(self, encoded_data: bytes, huffman_dict: dict) -> list:
        padding = encoded_data[0]
        encoded = ''.join(f'{byte:08b}' for byte in encoded_data[1:])
        encoded = encoded[:-padding] if padding else encoded
        reverse_huffman_dict = {v: k for k, v in huffman_dict.items()}

        decoded = []
        code = ""
        for bit in encoded:
            code += bit
            if code in reverse_huffman_dict:
                decoded.append(reverse_huffman_dict[code])
                code = ""
        return decoded
