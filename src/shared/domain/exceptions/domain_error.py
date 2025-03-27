from abc import ABC, abstractmethod


class DomainError(Exception, ABC):
    @property
    @abstractmethod
    def type(self) -> str: ...

    @property
    @abstractmethod
    def message(self) -> str: ...

    def to_primitives(self) -> dict:
        return {
            "type": self.type,
            "message": self.message,
        }
