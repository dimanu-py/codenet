from abc import ABC, abstractmethod


class TokenIssuer(ABC):
    @abstractmethod
    async def generate_token(self, account_id: str) -> dict:
        raise NotImplementedError
