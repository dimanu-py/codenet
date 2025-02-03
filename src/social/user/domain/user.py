from src.social.user.domain.user_id import UserId
from src.social.user.domain.user_name import UserName
from src.social.user.domain.user_username import UserUsername


class User:
    email: str
    username: UserUsername
    name: UserName
    id_: UserId

    def __init__(
        self, id_: UserId, name: UserName, username: UserUsername, email: str
    ) -> None:
        self.id_ = id_
        self.name = name
        self.username = username
        self.email = email

    def __eq__(self, other_user: "User") -> bool:
        return self.id_ == other_user.id_

    @classmethod
    def signup(cls, id_: str, name: str, username: str, email: str) -> "User":
        return User(
            id_=UserId(id_),
            name=UserName(name),
            username=UserUsername(username),
            email=email,
        )
