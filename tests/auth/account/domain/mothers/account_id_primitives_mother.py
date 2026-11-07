from object_mother import StringUuidPrimitivesMother


class AccountIdPrimitivesMother:
    @staticmethod
    def any() -> str:
        return StringUuidPrimitivesMother.any()

    @staticmethod
    def dummy() -> str:
        return "8d191aec-d821-4be7-b637-d33bddc6039e"
