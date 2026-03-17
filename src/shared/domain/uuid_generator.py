from abc import ABC, abstractmethod


class UuidGenerator(ABC):
    @abstractmethod
    def random(self) -> str:
        raise NotImplementedError
