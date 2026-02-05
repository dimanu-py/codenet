from sindripy.mothers import ObjectMother, StringUuidPrimitivesMother


class AccountMother(ObjectMother):
    @classmethod
    def any(cls) -> dict:
        return {
            "id": StringUuidPrimitivesMother.any(),
            "email": cls._faker().email(),
            "plain_password": cls._faker().password(),
            "status": "active",
            "created_at": cls._faker().iso8601(),
        }
