from typing import Self

from src.social.user.domain.user_email import UserEmail
from src.social.user.domain.user_id import UserId
from src.social.user.domain.user_name import UserName
from src.social.user.domain.user_username import UserUsername


class User:
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

    def __eq__(self, other_user: Self) -> bool:
        return self._id == other_user._id

    @property
    def id(self) -> UserId:
        return self._id

    @property
    def username(self) -> UserUsername:
        return self._username

    @classmethod
    def signup(cls, id: str, name: str, username: str, email: str) -> Self:
        return User(
            id=UserId(id),
            name=UserName(name),
            username=UserUsername(username),
            email=UserEmail(email),
        )

    def to_primitives(self) -> dict:
        return {
            "id": self._id.value,
            "name": self._name.value,
            "username": self._username.value,
            "email": self._email.value,
        }
