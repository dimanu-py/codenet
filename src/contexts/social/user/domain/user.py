from typing import override

from src.contexts.social.user.domain.user_email import UserEmail
from src.contexts.social.user.domain.user_full_name import UserFullName
from src.contexts.social.user.domain.user_id import UserId
from src.contexts.social.user.domain.user_name import UserName
from src.contexts.social.user.domain.user_profile_picture import UserProfilePicture


class User:
    _id: UserId
    _name: UserFullName
    _username: UserName
    _email: UserEmail
    _profile_picture: UserProfilePicture

    def __init__(
        self,
        id_: UserId,
        name: UserFullName,
        username: UserName,
        email: UserEmail,
        profile_picture: UserProfilePicture,
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
            username=UserName(username),
            email=UserEmail(email),
            profile_picture=UserProfilePicture(profile_picture),
        )

    @property
    def id(self) -> UserId:
        return self._id

    @override
    def __eq__(self, other: "User") -> bool:
        return self._id == other.id
