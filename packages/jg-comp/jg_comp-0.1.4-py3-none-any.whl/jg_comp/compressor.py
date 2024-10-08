# jg_comp/compressor.py
import collections
from concurrent.futures import ThreadPoolExecutor
from .huffman import HuffmanEncoder
from .matching import DictionaryMatcher
from .utils import split_data_for_parallel_processing

from concurrent.futures import ThreadPoolExecutor

class Compressor:
    def __init__(self, min_match_length=3):
        self.min_match_length = min_match_length
        self.matcher = DictionaryMatcher(min_match_length)
        self.huffman = HuffmanEncoder()
        self.huffman_dict = None  # Initialize huffman_dict to None

    def compress(self, data: bytes) -> bytes:
        compressed_data = self.matcher.compress(data)
        compressed_data, huffman_dict = self.huffman.huffman_encode(compressed_data)
        self.huffman_dict = huffman_dict  # Store huffman_dict for later use
        return compressed_data

    def decompress(self, compressed_data: bytes) -> bytes:
        if self.huffman_dict is None:
            raise ValueError("Huffman dictionary not found. Ensure compression was done before decompression.")
        decompressed_data = self.huffman.huffman_decode(compressed_data, self.huffman_dict)
        return self.matcher.decompress(decompressed_data)