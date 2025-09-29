from typing import Callable, Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def validate(func: F | None = None, *, order: int = 0) -> Callable[[F], F] | F:
    """Mark a method as a validator for ValueObject validation.

    Arguments:
        func: the function to decorate.
        order: order in which this validator should run relative to other validators in the same class. Lower numbers run first.
    """

    def wrapper(fn: F) -> F:
        if type(order) is not int:
            raise TypeError(
                f"Validation order {order} must be an integer. Got {type(order).__name__} type."
            )
        if order < 0:
            raise ValueError(f"Validation order {order} must be a positive value.")

        setattr(fn, "_is_validator", True)
        setattr(fn, "_order", order)
        return fn

    if func is not None:
        return wrapper(func)

    return wrapper
