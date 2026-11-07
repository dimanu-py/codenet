from src.auth.account.domain.account import AccountPrimitives
from src.auth.account.domain.account_signed_up import AccountSignedUp, AccountSignedUpAttributes


class AccountSignedUpMother:
    @staticmethod
    def from_account(account: AccountPrimitives) -> AccountSignedUp:
        account.pop("password")
        return AccountSignedUp(
            id=account["id"],
            occurred_at=account["created_at"],
            attributes=AccountSignedUpAttributes(**account),
        )
