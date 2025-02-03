from src.social.user.domain.user_id import UserId


class User:
    email: str
    username: str
    name: str
    id_: UserId

    def __init__(self, id_: UserId, name: str, username: str, email: str) -> None:
        self.id_ = id_
        self.name = name
        self.username = username
        self.email = email

    def __eq__(self, other_user: "User") -> bool:
        return self.id_ == other_user.id_

    @classmethod
    def signup(cls, id_: str, name: str, username: str, email: str) -> "User":
        return User(id_=UserId(id_), name=name, username=username, email=email)
