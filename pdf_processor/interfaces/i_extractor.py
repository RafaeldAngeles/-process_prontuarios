from abc import ABC, abstractmethod

class IExtractor(ABC):
    @abstractmethod
    def extract(self, text: str) -> dict:
        pass
