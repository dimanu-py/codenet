from typing import TypedDict


class AuthenticationToken(TypedDict):
    access_token: str
    token_type: str
    expires_in: int
