from src.shared.domain.value_objects.aggregate import Aggregate
from src.social.user.domain.user_email import UserEmail
from src.social.user.domain.user_id import UserId
from src.social.user.domain.user_name import UserName
from src.social.user.domain.user_username import UserUsername


class User(Aggregate):
    _id: UserId
    _name: UserName
    _username: UserUsername
    _email: UserEmail

    def __init__(self, id: str, name: str, username: str, email: str) -> None:
        self._id = UserId(id)
        self._name = UserName(name)
        self._username = UserUsername(username)
        self._email = UserEmail(email)

    @property
    def id(self) -> UserId:
        return self._id

    @property
    def username(self) -> UserUsername:
        return self._username
