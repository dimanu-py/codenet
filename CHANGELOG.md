## v0.1.0 (2025-02-11)

### Feat

- **user**: add id property to User to avoid direct accessing its attributes
- **user**: add to_aggregate method to UserModel to be able to convert database data into domain model
- **user**: implement search method in PostgresUserRepository
- **user**: add search abstractmethod to UserRepository
- **user**: concrete implementation of UserRepository using Postgres

### Fix

- **shared**: specify in database url that asyncpg must be used instead of pyscopg

### Refactor

- **user**: extract async engine generation to function and injected into router
- **user**: create async fixture to yield an engine and be able to create and delete tables on every test
- **user**: remove the use of SessionMaker and pass directly an AsyncEngine
- **shared**: create async engines and sessions with SQLAlchemy instead of working with synchronous operations
- **user**: extract semantic methods in acceptance test
- **user**: remove unused InMemoryUserRepository
- **user**: use PostgresUserRepository inside router instead of in memory
