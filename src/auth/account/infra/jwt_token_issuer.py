from typing import override

from src.auth.account.domain.token_issuer import TokenIssuer


class JwtTokenIssuer(TokenIssuer):
    @override
    async def generate_token(self, identification: str) -> dict:
        pass
