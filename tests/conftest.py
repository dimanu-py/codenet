pytest_plugins = [
    "tests.shared.delivery.fastapi_fixtures",
    "tests.shared.infra.persistence.database_fixtures",
    "tests.shared.infra.injector.di_fixtures",
    "tests.backoffice.user.user_fixtures",
    "tests.auth.account.account_fixtures",
]
