from typing import override

from src.contexts.social.user.domain.user_full_name import UserFullName
from src.contexts.social.user.domain.user_id import UserId


class User:
    _id: UserId
    _name: UserFullName
    _username: str
    _email: str
    _profile_picture: str

    def __init__(
        self,
        id_: UserId,
        name: UserFullName,
        username: str,
        email: str,
        profile_picture: str,
    ) -> None:
        self._id = id_
        self._name = name
        self._username = username
        self._email = email
        self._profile_picture = profile_picture

    @classmethod
    def create(
        cls, id_: str, name: str, username: str, email: str, profile_picture: str
    ) -> "User":
        return User(
            id_=UserId(id_),
            name=UserFullName(name),
            username=username,
            email=email,
            profile_picture=profile_picture,
        )

    @property
    def id(self) -> UserId:
        return self._id

    @override
    def __eq__(self, other: "User") -> bool:
        return self._id == other.id
