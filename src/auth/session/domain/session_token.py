from typing import TypedDict


class SessionToken(TypedDict):
    access_token: str
    token_type: str
    expires_in: int
