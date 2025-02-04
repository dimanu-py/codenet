import inspect

from tests.social.shared.expects.async_expectation import AsyncExpectation


def async_expect(subject):
    return AsyncExpectation(subject)


class raise_error:
    def __init__(self, exception_type):
        self._exception_type = exception_type

    async def _match_async(self, subject):
        if not callable(subject):
            return False, ["Subject is not callable"]

        try:
            coro = subject()
            if not inspect.isawaitable(coro):
                return False, ["Subject did not return a coroutine"]

            await coro
        except self._exception_type:
            return True, ["Raised the expected error"]
        except Exception as e:
            return (
                False,
                [
                    f"Expected {self._exception_type.__name__}, but got {type(e).__name__}: {str(e)}"
                ],
            )
        else:
            return (
                False,
                [f"Expected {self._exception_type.__name__}, but no error was raised"],
            )

    def _failure_message(self, subject, reasons):
        message = f"\nexpected: {subject!r} to {self!r}"

        if reasons:
            message += f"\n     but: {'\n'.join(reasons)}"

        return message
