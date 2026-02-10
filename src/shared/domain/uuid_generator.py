from abc import ABC, abstractmethod


class UuidGenerator(ABC):
    @classmethod
    @abstractmethod
    def random(cls) -> str:
        raise NotImplementedError
