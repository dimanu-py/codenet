from object_mother import ObjectMother


class UserNamePrimitivesMother(ObjectMother):
    @classmethod
    def any(cls) -> str:
        return cls._faker().name()
