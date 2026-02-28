import time
from typing import Any, override

import jwt

from src.auth.session.domain.token_issuer import TokenIssuer
from src.shared.delivery.settings import Settings


class JwtTokenIssuer(TokenIssuer):
    _TOKEN_TYPE = "bearer"

    def __init__(self, settings: Settings) -> None:
        self._secret_key = settings.jwt_secret_key
        self._algorithm = settings.jwt_algorithm
        self._expires_in = settings.jwt_expires_in

    @override
    async def generate_token(self, identification: str) -> dict[str, Any]:
        now = int(time.time())
        payload = {
            "sub": identification,
            "iat": now,
            "exp": now + self._expires_in,
        }
        token = jwt.encode(payload, self._secret_key, algorithm=self._algorithm)
        return {
            "access_token": token,
            "token_type": self._TOKEN_TYPE,
            "expires_in": self._expires_in,
        }
