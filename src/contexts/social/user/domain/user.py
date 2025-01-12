from typing import override


class User:
    _id: str
    _name: str
    _username: str
    _email: str
    _profile_picture: str

    def __init__(
        self, id_: str, name: str, username: str, email: str, profile_picture: str
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
            id_=id_,
            name=name,
            username=username,
            email=email,
            profile_picture=profile_picture,
        )

    @property
    def id(self) -> str:
        return self._id

    @override
    def __eq__(self, other: "User") -> bool:
        return self._id == other.id
