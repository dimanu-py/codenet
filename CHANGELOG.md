## v0.2.0 (2025-02-11)

### Feat

- **user**: log when a request to user signup gets processed correctly
- **user**: log when a domain error is raised
- **user**: log requests received to sign up user route
- **shared**: implement logic to create a logger with two handlers for dev and production
- **shared**: add custom log formatter
- **app**: add custom handler to catch unexpected exceptions
- **user**: wrap use case call within try-except block and handle domain errors

### Refactor

- **shared**: forced log folder to be at the root of the project
- **shared**: rename http response module file
- **shared**: move modules related to http to specific package
- **user**: let test method receive the request in the call

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
