from object_mother import ObjectMother


class AccountUsernamePrimitivesMother(ObjectMother):
    @classmethod
    def any(cls) -> str:
        return cls._faker().user_name()

    @staticmethod
    def dummy() -> str:
        return "dummy.username"
