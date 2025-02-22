## v0.4.0 (2025-02-22)

### Feat

- **user**: create user search response object
- **shared**: implement logic to generate a where equality clause in converter
- **shared**: add is_empty method to criteria to know if it has filters or not
- **shared**: implement basic select query with no filters
- **user**: design how I want matching method to work in SQL
- **user**: add username property to User
- **user**: define matching method in UserRepository
- **user**: design interaction with repository and criteria inside the use case
- **user**: create Criteria object
- **user**: wrap Filter collection inside Filters object
- **user**: create Filter object to group the combination of field, value and operator
- **user**: create FilterOperator enum to store all possible operations
- **user**: create FilterValue object to store the value the client will search
- **user**: create FilterField to store the field the user will be searched by
- **user**: create SearchUserQuery to store query parameters
- **user**: create UserSearcher use case
- **user**: design interaction between router and use case

### Refactor

- **user**: work with UserSearchResponse in HttpResponse
- **user**: avoid iterating again over searched_users list as UserRepository already returns them as a list of aggregates
- **shared**: move stringify method to test class as it's only needed to be able to compare string queries and sqlalchemy does not process raw strings
- **shared**: extract common method to compile query into string for criteria converter
- **shared**: early return when criteria is empty
- **user**: rename test variable to express that what is returned is a collection of users
- **user**: return empty list when no user is found instead of None
- **user**: rename User field attributes to make them protected
- **user**: allow UserMother to be created with fixed values passing a dictionary instead of coupling it to a command
- **user**: add to_dict method to UserSignupCommand

## v0.3.0 (2025-02-18)

### Feat

- **http**: create POST request example to try application manually
- **api**: implement lifespan to manage migration event on startup
- **api**: create class to be able to perform migrations on startup
- **migrations**: create first migration that creates user table
- **migrations**: override sqlalchemy.url variable with custom url using Settings class
- **migrations**: add project Base metadata in alembic environment
- **migrations**: enable ruff to format and lint revisions scripts
- **migrations**: specify a time format for revision files so they appear ordered
- **migrations**: initialize alembic environment to manage migrations

### Fix

- **migrations**: import all sqlalchemy models so alembic detects correctly changes

### Refactor

- **user**: remove the use of the logger inside endpoint and pass resource to logged when request is successful
- **api**: pass exception when internal server error is raised so it can be logged
- **shared**: log error and request information inside HttpResponse class
- **user**: use context manager to be able to perform startup event on acceptance test
- **user**: remove table creation from engine_generator and encapsulate it between a try-finally clause
- **user**: write correct type hint for engine_generator

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
