class AccountWithUserSignup:
    async def execute(
        self,
        account_id,
        name,
        username,
        email,
        password,
    ) -> None:
        raise NotImplementedError
