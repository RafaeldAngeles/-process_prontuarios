from abc import ABC, abstractmethod

class IRepository(ABC):
    @abstractmethod
    def save(self, data: dict) -> None:
        pass
