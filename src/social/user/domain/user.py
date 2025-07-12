from typing import Self

from src.shared.domain.value_objects.aggregate import Aggregate
from src.social.user.domain.user_email import UserEmail
from src.social.user.domain.user_id import UserId
from src.social.user.domain.user_name import UserName
from src.social.user.domain.user_username import UserUsername


class User(Aggregate):
    _email: UserEmail
    _username: UserUsername
    _name: UserName
    _id: UserId

    def __init__(
        self, id: UserId, name: UserName, username: UserUsername, email: UserEmail
    ) -> None:
        self._id = id
        self._name = name
        self._username = username
        self._email = email

    @property
    def id(self) -> UserId:
        return self._id

    @property
    def username(self) -> UserUsername:
        return self._username

    @classmethod
    def signup(cls, id: str, name: str, username: str, email: str) -> Self:
        return cls(
            id=UserId(id),
            name=UserName(name),
            username=UserUsername(username),
            email=UserEmail(email),
        )
