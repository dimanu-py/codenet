from abc import ABC, abstractmethod


class TokenIssuer(ABC):
    @abstractmethod
    async def generate_token(self, identification: str) -> dict:
        raise NotImplementedError
