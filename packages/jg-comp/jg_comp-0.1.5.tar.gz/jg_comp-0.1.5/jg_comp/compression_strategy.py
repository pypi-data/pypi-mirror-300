# jg_comp/compression_strategy.py
from abc import ABC, abstractmethod

class CompressionStrategy(ABC):
    """Abstract base class for compression strategies."""

    @abstractmethod
    def compress(self, data: bytes) -> bytes:
        pass

    @abstractmethod
    def decompress(self, data: bytes) -> bytes:
        pass
