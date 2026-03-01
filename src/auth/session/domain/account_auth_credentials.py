from dataclasses import dataclass


@dataclass(frozen=True)
class AccountAuthCredentials:
    account_id: str
    password: str
    status: str
