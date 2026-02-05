class AccountWithUserSignup:
    async def execute(
        self,
        account_id: str,
        name: str,
        username: str,
        email: str,
        password: str,
    ) -> None:
        await self._signup_account_with(
            account_id=account_id,
            email=email,
            plain_password=password,
        )
        await self._signup_user_with(
            user_id=account_id,
            name=name,
            username=username,
            email=email,
        )

    async def _signup_user_with(self, user_id: str, name: str, username: str, email: str) -> None:
        pass

    async def _signup_account_with(self, account_id: str, email: str, plain_password: str) -> None:
        pass