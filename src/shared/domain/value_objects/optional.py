_EMPTY = object()


class Optional[T]:
    __slots__ = ("_value",)

    def __init__(self, value: object = _EMPTY) -> None:
        self._value = value

    @classmethod
    def of(cls, value: T) -> "Optional[T]":
        if value is None:
            raise ValueError("Optional.of(None) is not valid. Use Optional.nothing() instead.")
        return cls(value)

    @classmethod
    def empty(cls) -> "Optional[T]":
        return cls(_EMPTY)

    def is_present(self) -> bool:
        return self._value is not _EMPTY

    def is_empty(self) -> bool:
        return self._value is _EMPTY
