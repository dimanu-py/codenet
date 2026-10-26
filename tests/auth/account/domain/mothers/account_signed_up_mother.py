from src.auth.account.domain.account import Account
from src.auth.account.domain.account_signed_up import AccountSignedUp, AccountSignedUpAttributes


class AccountSignedUpMother:
    @staticmethod
    def from_account(account: Account) -> AccountSignedUp:
        account_primitives = account.to_primitives(exclude="password")
        return AccountSignedUp(
            id=account_primitives["id"],
            occurred_at=account_primitives["created_at"],
            attributes=AccountSignedUpAttributes(**account_primitives),
        )
