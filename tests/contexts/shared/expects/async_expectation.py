from expects.expectations import Expectation


class AsyncExpectation(Expectation):
    async def to(self, matcher):
        """Same idea as original Expectation.to, but we await the assertion.

        usage -> await async_expect(...).to(...)
        """
        __tracebackhide__ = True
        await self._assert(matcher)

    async def not_to(self, matcher):
        """Same idea as original Expectation.not_to, but we await the assertion.

        usage -> await async_expect(...).not_to(...)
        """
        __tracebackhide__ = True
        self._negated = True
        await self.to(matcher)

    async def _assert(self, matcher):
        """Same idea as original Expectation._assert, but we await the assertion."""
        __tracebackhide__ = True
        ok, reasons = await self._match(matcher)
        if not ok:
            raise AssertionError(self._failure_message(matcher, reasons))

    async def _match(self, matcher):
        """Evaluates if async condition is met.

        1. Determine if we should call the negated or normal match.
        2. If the matcher has an async version, call that. Otherwise,
           call the synchronous version from the base class.
        """
        method_suffix = "_negated_async" if self._negated else "_async"
        async_method_name = f"_match{method_suffix}"

        if hasattr(matcher, async_method_name):
            return await getattr(matcher, async_method_name)(self._subject)
        else:
            return super()._match(matcher)
