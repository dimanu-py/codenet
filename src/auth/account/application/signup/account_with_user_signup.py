class AccountWithUserSignup:
    async def execute(
        self,
        account_id: str,
        name: str,
        username: str,
        email: str,
        password: str,
    ) -> None:
        raise NotImplementedError
