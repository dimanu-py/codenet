class AccountAuthenticator:
    async def execute(self, identification: str, password: str) -> str:
        raise NotImplementedError
