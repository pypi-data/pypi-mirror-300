# jg_comp/compressor.py
import collections
from concurrent.futures import ThreadPoolExecutor
from .huffman import HuffmanEncoder
from .matching import DictionaryMatcher
from .utils import split_data_for_parallel_processing

class Compressor:
    def __init__(self, min_match_length=3):
        self.min_match_length = min_match_length
        self.matcher = DictionaryMatcher(min_match_length)
        self.huffman = HuffmanEncoder()

    def compress(self, data: bytes) -> bytes:
        compressed_data = self.matcher.compress(data)
        compressed_data, huffman_dict = self.huffman.huffman_encode(compressed_data)
        self.huffman_dict = huffman_dict
        return compressed_data

    def decompress(self, compressed_data: bytes) -> bytes:
        decompressed_data = self.huffman.huffman_decode(compressed_data, self.huffman_dict)
        return self.matcher.decompress(decompressed_data)

    def parallel_compress(self, data: bytes, num_threads: int = 4) -> bytes:
        """Compress data using parallel processing."""
        chunks = split_data_for_parallel_processing(data, num_threads)
        compressed_chunks = []

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            results = executor.map(self.compress, chunks)

        compressed_data = []
        for result in results:
            compressed_data.extend(result)
        return bytes(compressed_data)
