from typing import Any, TypeVar

from doublex import Mimic, Stub

T = TypeVar("T")


class AsyncStub:
    """
    A wrapper around doublex Stub that makes async methods work properly.

    This class allows you to use doublex's familiar stubbing syntax while
    ensuring that async methods return coroutines that can be awaited.

    You can use when() directly on the AsyncStub instance.

    Example:
        user_signup = AsyncStub(UserSignup)
        when(user_signup).execute(ANY_ARG).returns(None)

        # Now this will work:
        await user_signup.execute(command)
    """

    def __init__(self, target_class: type[T]):
        """
        Initialize AsyncStub for a target class.

        Args:
            target_class: The class to create a stub for
        """
        stub = Mimic(Stub, target_class)
        object.__setattr__(self, "_stub", stub)
        object.__setattr__(self, "_async_cache", {})

    def __getattr__(self, name: str) -> Any:
        """
        Intercept attribute access to wrap async methods.

        This allows both doublex's when() to configure the stub and
        actual async calls to work properly.
        """
        # Get the attribute from the underlying stub
        attr = getattr(self._stub, name)

        # If it's a method, we need to wrap it to return an awaitable
        if callable(attr) and not name.startswith("_"):
            # Check if we've already created an async wrapper for this method
            cache = object.__getattribute__(self, "_async_cache")
            if name not in cache:
                # Create an async wrapper that calls the stub method
                # and returns the result (which can be awaited)
                async def async_method(*args: Any, **kwargs: Any) -> Any:
                    stub = object.__getattribute__(self, "_stub")
                    result = getattr(stub, name)(*args, **kwargs)
                    return result

                cache[name] = async_method

            return cache[name]

        return attr

    def __setattr__(self, name: str, value: Any) -> None:
        """Forward attribute setting to the underlying stub."""
        setattr(self._stub, name, value)

    def __repr__(self) -> str:
        """Return a representation of the AsyncStub."""
        return f"AsyncStub({self._stub!r})"

    # These methods allow doublex's when() to work with AsyncStub directly
    def __doublex__(self) -> Any:
        """Return the underlying stub for doublex integration."""
        return self._stub

    def __doublex_stub__(self) -> Any:
        """Return the underlying stub for doublex integration."""
        return self._stub

    @property
    def __class__(self) -> type:
        """Proxy the class to the underlying stub for isinstance checks."""
        return self._stub.__class__
