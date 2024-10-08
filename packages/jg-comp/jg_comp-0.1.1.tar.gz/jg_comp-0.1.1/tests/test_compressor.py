# tests/test_compressor.py
import unittest
from jg_comp.compressor import Compressor
from jg_comp.matching import DictionaryMatcher

class TestCompressor(unittest.TestCase):

    def test_compress_decompress(self):
        strategy = DictionaryMatcher()
        compressor = Compressor(strategy)
        data = b"this is some test data to compress"
        compressed_data = compressor.compress(data)
        decompressed_data = compressor.decompress(compressed_data)
        self.assertEqual(decompressed_data, data)

if __name__ == "__main__":
    unittest.main()
