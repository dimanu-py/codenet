from argon2 import PasswordHasher
from sindripy.mothers import ObjectMother


class AccountPasswordHashPrimitivesMother(ObjectMother):
    _HASHER = PasswordHasher(
        time_cost=2,
        memory_cost=65536,
        parallelism=4,
    )

    @classmethod
    def any(cls) -> str:
        plain_password = cls._faker().password()
        return cls._HASHER.hash(plain_password)

    @classmethod
    def from_plain_password(cls, plain_password: str) -> str:
        return cls._HASHER.hash(plain_password)
