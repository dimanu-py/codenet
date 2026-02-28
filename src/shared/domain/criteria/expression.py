from abc import ABC, abstractmethod
from typing import Self


class Expression(ABC):
    @abstractmethod
    def from_primitives(self, expression: dict[str, list | str]) -> Self:
        raise NotImplementedError

    @abstractmethod
    def to_primitives(self) -> dict[str, list | str]:
        raise NotImplementedError
