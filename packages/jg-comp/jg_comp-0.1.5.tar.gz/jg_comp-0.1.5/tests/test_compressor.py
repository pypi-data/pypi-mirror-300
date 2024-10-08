# tests/test_compressor.py
import sys
import time
import unittest
from jg_comp.compressor import Compressor
from jg_comp.matching import DictionaryMatcher

class TestCompressor(unittest.TestCase):

    def test_compress_decompress(self):
        compressor = Compressor()
        data = b"this is some test data to compress"
        compressed_data = compressor.compress(data)
        decompressed_data = compressor.decompress(compressed_data)
        self.assertEqual(decompressed_data, data)

    def test_compress_decompress_with_text(self):
        # Sample text
        text = """
        In a mountain village, at the foot of an ancient forest, lived people who had learned
        to respect nature and its creatures. The giant trees stood like silent guardians, sheltering
        birds, foxes, and other animals in their thick branches and twisted roots.

        Each morning, the villagers would gather to admire the beauty around them. The children played
        around the trunks, inventing stories about the spirits of the trees, while the elders told
        legends passed down through generations.

        Life in the village was simple, but full of magic. The seasons passed, each bringing its own
        wonders: wildflowers in the spring, juicy fruits in the summer, vibrant colors in the fall, and
        snow that blanketed everything in white in the winter.
        """
        
        # Encode the text as bytes
        data_bytes = text.encode('utf-8')
        
        compressor = Compressor()

        # Generic function for compression and decompression
        def compress_and_decompress(algorithm_name, compress_function, decompress_function, data):
            # Measure compression time
            t0 = time.time()
            compressed_data = compress_function(data)
            t1 = time.time()
            compression_time = t1 - t0

            # Measure decompression time
            t0 = time.time()
            decompressed_data = decompress_function(compressed_data)
            t1 = time.time()
            decompression_time = t1 - t0

            # Convert decompressed data to text if possible
            if isinstance(decompressed_data, bytes):
                try:
                    decompressed_text = decompressed_data.decode('utf-8')
                except UnicodeDecodeError as e:
                    decompressed_text = f"Decoding error: {e}"
            else:
                decompressed_text = f"Unexpected format: {type(decompressed_data)}"

            # Print the results
            print_comparison_results(algorithm_name, compressed_data, decompressed_text, compression_time, decompression_time)

        # Function to print results and decompressed text
        def print_comparison_results(algorithm_name, compressed_data, decompressed_text, compression_time, decompression_time):
            original_size = len(data_bytes)
            compressed_size = len(compressed_data)
            compression_ratio = original_size / compressed_size if compressed_size > 0 else float('inf')
            memory_usage = sys.getsizeof(compressed_data)
            decompression_success = text == decompressed_text

            # Calculate size reduction percentage
            size_reduction = ((original_size - compressed_size) / original_size) * 100

            # Calculate compression and decompression speeds
            compression_speed = original_size / compression_time if compression_time > 0 else float('inf')
            decompression_speed = original_size / decompression_time if decompression_time > 0 else float('inf')

            print(f"\n=== Compression Results with {algorithm_name} ===")
            print(f"Original data size: {original_size} bytes")
            print(f"Compressed data size: {compressed_size} bytes")
            print(f"Compression time: {compression_time:.6f} seconds")
            print(f"Decompression time: {decompression_time:.6f} seconds")
            print(f"Compression ratio: {compression_ratio:.2f}")
            print(f"Size reduction: {size_reduction:.2f}%")
            print(f"Compression speed: {compression_speed:.2f} bytes/second")
            print(f"Decompression speed: {decompression_speed:.2f} bytes/second")
            print(f"Decompression successful: {decompression_success}")
            # Display the first 500 characters of the decompressed text
            print(f"Decompressed text (first 500 characters):\n{decompressed_text[:500]}...\n")

        # List of algorithms and their compression/decompression functions
        algorithms = [
            ("Compressor", compressor.compress, compressor.decompress)
        ]

        # Compression and decompression with each algorithm
        for algorithm_name, compress_function, decompress_function in algorithms:
            compress_and_decompress(algorithm_name, compress_function, decompress_function, data_bytes)


if __name__ == "__main__":
    unittest.main()
