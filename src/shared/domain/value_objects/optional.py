_NOTHING = object()


class Optional[T]:
    __slots__ = ("_value",)

    def __init__(self, value: object = _NOTHING) -> None:
        self._value = value

    @classmethod
    def of(cls, value: T) -> "Optional[T]":
        return cls(value)

    def is_present(self) -> bool:
        return self._value is not _NOTHING
