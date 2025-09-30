# CHANGELOG

<!-- version list -->

## v1.3.0 (2025-09-30)

### ✨ Features

- **migration**: Generate migration script modifying id column in users table
  ([`a62b551`](https://github.com/dimanu-py/codenet/commit/a62b5515cb7f89485bf11b74bc380858501d92d2))

- **user**: Remove not needed engine_generator function and implement new function to be able to
  inject an async session to the postgres user repository
  ([`f632904`](https://github.com/dimanu-py/codenet/commit/f632904180f707817eeecc3e1c8d5690cb1e1529))

- **user**: Implement session-based user deletion in PostgresUserRepository
  ([`a4a0c3d`](https://github.com/dimanu-py/codenet/commit/a4a0c3da3d772640050345e4c5ffecd1f9d4d9a2))

- **user**: Optimize matching method to utilize session when available
  ([`6a15624`](https://github.com/dimanu-py/codenet/commit/6a15624642cc339492aea93c85c5bf5e9664cf72))

- **user**: Extend PostgresUserRepository's save and find method to use session attribute when is
  available
  ([`12c6fe9`](https://github.com/dimanu-py/codenet/commit/12c6fe9676c0a50b1e6a58cbee105542db1373f9))

- **user**: Include session dependency as optional to PostgresUserRepository
  ([`524ddb9`](https://github.com/dimanu-py/codenet/commit/524ddb96bf00655e1b8dbdf32e2dd55a1952b440))

- **delivery**: Add correlation id middleware to main application
  ([`09587bd`](https://github.com/dimanu-py/codenet/commit/09587bd66b6d0234b60e611aa554ead292d1e9f8))

- **shared**: Include correlation id filter and data when logging
  ([`70b37fc`](https://github.com/dimanu-py/codenet/commit/70b37fc861afd6e08657eeb62a63fe3547d0ecd8))

- **user**: Create file to have common dependencies for user aggregate endpoints
  ([`3e300b4`](https://github.com/dimanu-py/codenet/commit/3e300b482d812433f6e06fb13cf61a92c50cda2b))

- **user**: Update path parameters to use 'examples' as 'example' has been deprecated
  ([`896744f`](https://github.com/dimanu-py/codenet/commit/896744f8c6f27dbdec2c4a934af1b1933846fa50))

- **user**: Modify endpoint names to use nouns instead of verbs or actions
  ([`3612be8`](https://github.com/dimanu-py/codenet/commit/3612be8e93ea20367387f4b39ab917945a17396c))

- **user**: Replace SuccessResponse with specific response classes for user removal, search, and
  signup endpoints
  ([`be93d99`](https://github.com/dimanu-py/codenet/commit/be93d991405cd0e8e175f179432d0939c20bfe4a))

- **shared**: Extend SuccessResponse to include specific response classes for Created, Ok, and
  Accepted statuses
  ([`ec1e61a`](https://github.com/dimanu-py/codenet/commit/ec1e61a22da9922bc695a4d4a099bcedb275ceef))

- **user**: Add example to user_id path parameter in signup user endpoint
  ([`f204fd8`](https://github.com/dimanu-py/codenet/commit/f204fd8cd7433e6eee4d1a4c7c008d768b867ae9))

- **user**: Add example to filter query parameter in get_user_by_criteria
  ([`ef1eac7`](https://github.com/dimanu-py/codenet/commit/ef1eac7f92238ecbd325992bda46406fb0fbec19))

### 🪲 Bug Fixes

- **user**: Modify UserModel database representation to store id as a string of max length 36
  instead of UUID
  ([`183be4c`](https://github.com/dimanu-py/codenet/commit/183be4c302aeafabeccd6523cac9856987ab8f45))

- **shared**: Set status code for CreatedResponse correctly to 201
  ([`2df6401`](https://github.com/dimanu-py/codenet/commit/2df640134cb597419187a0ea602b18777f131f78))

### ♻️ Refactoring

- **delivery**: Ignore type error when adding middlewares
  ([`603e9ed`](https://github.com/dimanu-py/codenet/commit/603e9ed1fdf385f3f533c6720868564168998ceb))

- **shared**: Fix type errors
  ([`3e937e7`](https://github.com/dimanu-py/codenet/commit/3e937e74306bef9003e70711faed6a3b1a42ad2f))

- **user**: Remove engine argument from PostgresUserRepository constructor
  ([`e2caeb8`](https://github.com/dimanu-py/codenet/commit/e2caeb8c89e16437a9921fbdc9af6dd658fc9187))

- **user**: Remove all uses of session maker
  ([`926e8ec`](https://github.com/dimanu-py/codenet/commit/926e8ec50f0be6295035e34a595463907a05847c))

- **user**: Update endpoints to use new 'postgres_user_repository' function to inject concrete user
  repository to endpoints
  ([`6b33147`](https://github.com/dimanu-py/codenet/commit/6b33147f00c39e3763fcd34c3f59c5bd60804e3b))

- **user**: Move domain errors to their closest class files to keep information cohesive
  ([`f96e08b`](https://github.com/dimanu-py/codenet/commit/f96e08ba93261569076aa7d71fd031ba9de83c74))

- **user**: Update domain and application errors to not define unnecessary fields
  ([`b52ad65`](https://github.com/dimanu-py/codenet/commit/b52ad6521e5ef363353d475ab43e3a1274c6a9b8))

- **user**: Remove named constructor 'signup' from User and leave a single init method
  ([`5568515`](https://github.com/dimanu-py/codenet/commit/55685158ce5b2e56d7e856c16547fa378705a10e))

- **shared**: Update base value object to manage validation in the order specified by the decorators
  ([`4e80ef9`](https://github.com/dimanu-py/codenet/commit/4e80ef93f9692242573dd2f5717020303e14de91))

- **shared**: Modify validate decorator to be applied to value object allowing to specify the order
  of the validation
  ([`3f540b2`](https://github.com/dimanu-py/codenet/commit/3f540b224181702db2098fd7720239f8541abee5))

- **shared**: Modify basic domain errors to not set unnecessary fields when creating them
  ([`c20342c`](https://github.com/dimanu-py/codenet/commit/c20342ca716c929315cacc25ec13f3de0d5d065b))


## v1.1.0 (2025-07-12)

### ✨ Features

- **user**: Make User inherit from Aggregate base class
  ([`9223aab`](https://github.com/dimanu-py/social-network/commit/9223aabed65896614973bcba4a9a5b85900075e2))

- **shared**: Define base abstract class to represent aggregates
  ([`378737d`](https://github.com/dimanu-py/social-network/commit/378737d28d6c02f14dfc561feef05505866d2dcb))

- **shared**: Add decorator to mark all methods of value object that should be considered when
  validating
  ([`eccbf20`](https://github.com/dimanu-py/social-network/commit/eccbf20d46646e09cd5304833f959c98a4cb34f3))

- **shared**: Raise error when uuid value is none
  ([`cd9f01c`](https://github.com/dimanu-py/social-network/commit/cd9f01cc35944ccdbc154b8aa9e61e4883a5c4d3))

- **shared**: Add __match_args__ for improved pattern matching
  ([`f0c44fe`](https://github.com/dimanu-py/social-network/commit/f0c44fe1ed6c7bdf7854fd20e321826ff82be674))

- **shared**: Implement strategy pattern to be able to translate and, or and simple conditions to
  its sql query with sqlalchemy syntax
  ([`f10dc29`](https://github.com/dimanu-py/social-network/commit/f10dc298c6fe90996479237511b366c029ff89b1))

- **shared**: Implement condition interface
  ([`4c05c2b`](https://github.com/dimanu-py/social-network/commit/4c05c2b59be85e50b1c33979d9e97a275308cb28))

- **shared**: Remove filters.py
  ([`e554c8f`](https://github.com/dimanu-py/social-network/commit/e554c8f2d8bf51fa1286a5cdb59bfd73909919ac))

- **shared**: Implement new version of criteria pattern allowing for a DSL to make nested filters
  with AND and/or OR logic operations
  ([`8be92f9`](https://github.com/dimanu-py/social-network/commit/8be92f9493f027b379f550e90b0a68da74a66a32))

- **shared**: Remove old implementation of criteria pattern
  ([`653175d`](https://github.com/dimanu-py/social-network/commit/653175d6dd380e8d57fd532b5cb2fb2fb2bf6eb3))

- **user**: Create base router for all users endpoints
  ([`334e305`](https://github.com/dimanu-py/social-network/commit/334e3054d305d38de289405509167217e1192d5d))

- **user**: Import implemented classes in removal user and return empty dict if successful
  ([`5039282`](https://github.com/dimanu-py/social-network/commit/50392820bdae75fc3728368dd3098703df1a0605))

- **user**: Implement 'delete' method in PostgresUserRepository
  ([`0da5cb9`](https://github.com/dimanu-py/social-network/commit/0da5cb9d39bad2d70f653ef2b0f215d7bac99b3b))

- **user**: Implement UserNotFoundError domain error
  ([`0dc3a8b`](https://github.com/dimanu-py/social-network/commit/0dc3a8be27b64929814877d5ad4ad91f7af4e2ae))

- **user**: Add 'delete' signature method to UserRepository interface
  ([`db39d5a`](https://github.com/dimanu-py/social-network/commit/db39d5a89a0ea55e9e04dc606dc90950bcf1a8ff))

- **user**: Design how user remover use case deletes existing user
  ([`b11bf70`](https://github.com/dimanu-py/social-network/commit/b11bf7038c86264ff7e3661f77ca2112b22ce81b))

- **user**: Create UserRemover use case
  ([`65cff03`](https://github.com/dimanu-py/social-network/commit/65cff0348c50408ba821edf3a9c3723634eae10f))

- **user**: Implement UserRemovalCommand dto
  ([`19bb9d7`](https://github.com/dimanu-py/social-network/commit/19bb9d7d3b52786efe01c214d3671fdbc2d229b8))

- **user**: Define how removal endpoint will orchestrate operations to remove user
  ([`3ef534f`](https://github.com/dimanu-py/social-network/commit/3ef534f5e84dab9297e05e930c1a6034cdbad9f9))

- **delivery**: Include removal router in application
  ([`38cfd53`](https://github.com/dimanu-py/social-network/commit/38cfd530d4d47d13173bf739237d4b4885a8cdc4))

### 🪲 Bug Fixes

- **user**: Allow some special characters that are common on first names
  ([`67f8cb2`](https://github.com/dimanu-py/social-network/commit/67f8cb280383e656614b8fe39aa5fb170496710a))

- **shared**: Pass value when raising incorrect value type error in int value object validation
  ([`6758eb0`](https://github.com/dimanu-py/social-network/commit/6758eb0f77f3293f60f7e44af86dfe9a444174e6))

- **shared**: Pass value when raising incorrect value type error in string value object validation
  ([`3253cb2`](https://github.com/dimanu-py/social-network/commit/3253cb2b90af3dfef3abd956147455b4cc88d76c))

- **shared**: Update condition to retrieve operator dynamically from condition dict in SQL query
  strategy
  ([`9999777`](https://github.com/dimanu-py/social-network/commit/99997774ad72f2b9698601e4460076679b0b8c82))

- Correct mypy errors
  ([`5a41e26`](https://github.com/dimanu-py/social-network/commit/5a41e26e6312359f1d566ff13508a73cc0b6aadf))

- **user**: Verify removal router returns 200 instead of 202
  ([`98765e0`](https://github.com/dimanu-py/social-network/commit/98765e0a2c60bbc157f5c79f0c5481c893acc929))

- **user**: Modify 'should_remove' method of mock repository to only compare user id
  ([`b1fc4ab`](https://github.com/dimanu-py/social-network/commit/b1fc4ab3fd5ed7580493de660074c09e1050bf32))

- **user**: Update user removal logic to use UserId to delete from database
  ([`5a4a127`](https://github.com/dimanu-py/social-network/commit/5a4a1273bb08fdea9313b6f33acdcb7c412e0eab))

- **user**: Modify 'should_find' method of mock repository to only compare user id and return a full
  user
  ([`2e6dbcc`](https://github.com/dimanu-py/social-network/commit/2e6dbcc27f24ae52017d6a288fe37a58aec2c760))

- **user**: Add missing imports to removal endpoint
  ([`402ab4b`](https://github.com/dimanu-py/social-network/commit/402ab4b328fbc3b1b144d163541e187c1d8db706))

### ♻️ Refactoring

- **shared**: Move concrete value objects to usables folder to separate base classes/interfaces from
  those that will be use
  ([`92e5d16`](https://github.com/dimanu-py/social-network/commit/92e5d164446eb62bd6628cd5ea3887e2e3b81f9f))

- Fix lint errors
  ([`44bfe5e`](https://github.com/dimanu-py/social-network/commit/44bfe5e260aee186395f65ac0215638e30519cb4))

- **shared**: Modify value object implementation to get all methods marked as validate and simplify
  concrete value objects
  ([`dfed479`](https://github.com/dimanu-py/social-network/commit/dfed479ef3a48eb4165cd9dd9a4b1c98573f252a))

- **user**: Rename filters query param to filter
  ([`3d980c4`](https://github.com/dimanu-py/social-network/commit/3d980c4513d04735c3bef2ec543d8b3b5ce40dee))

- **shared**: Extract operator of ComparatorCondition getting the value of the keys of the passed
  dict that matches any of the supported operators instead of expecting the operator value to be
  always passed as the last element of the dict
  ([`1825817`](https://github.com/dimanu-py/social-network/commit/182581741f24d535872862209f96b6b25fb0b6ac))

- **shared**: Modify CriteriaToSqlalchemyConvert to delegate query translation to strategy pattern
  ([`6afc81c`](https://github.com/dimanu-py/social-network/commit/6afc81cfbb96f7fb9f879e8a1584dd19597df3e0))

- **shared**: Rename condition_strategies.py and its class to operator_to_sql_translate_strategy.py
  and remove ALL operator
  ([`9d1b059`](https://github.com/dimanu-py/social-network/commit/9d1b059162ac9e871d071940726bfd072442e7eb))

- **shared**: Make subtypes of conditions implement its interface
  ([`639cded`](https://github.com/dimanu-py/social-network/commit/639cdedd5d2ef57e76fa0394ca55df765c8671fc))

- **shared**: Move NestedLogicalCondition to condition folder as its represent a different type of
  condition
  ([`f4ecea5`](https://github.com/dimanu-py/social-network/commit/f4ecea586bc98baa6d0bad99001b0db8afd500ae))

- **shared**: Rename FilterExpression to NestedLogicalCondition
  ([`69a3d57`](https://github.com/dimanu-py/social-network/commit/69a3d57de650b0598ef83792a445d36b447964e4))

- **shared**: Rename Condition to ComparatorCondition
  ([`764fea9`](https://github.com/dimanu-py/social-network/commit/764fea9810b48d676a437b265dba736408f9bb18))

- **shared**: Move condition_strategies.py to infra
  ([`ffdefc2`](https://github.com/dimanu-py/social-network/commit/ffdefc2516ca053d3fdf3bd7f3ce6e50e8e395b7))

- Fix mypy errors
  ([`7943049`](https://github.com/dimanu-py/social-network/commit/7943049dd591d1f87ba6fc526bb5a27f3a02f7d6))

- **shared**: Modify value object implementation to not allow to modify its value once initialized
  ([`53cb6ff`](https://github.com/dimanu-py/social-network/commit/53cb6ff466f93974e3d35a3560de7d03053e697a))

- **shared**: Modify criteria dsl filters to be <operator>:<value> instead of separate fields
  ([`3c72e93`](https://github.com/dimanu-py/social-network/commit/3c72e9303191cefabb46f7f7be75233e32577662))

- **delivery**: Include user routes instead of all routers one by one
  ([`033963e`](https://github.com/dimanu-py/social-network/commit/033963ea16d8e4c8e068695117f8160de5143405))

- **user**: Rename use case from user removal to user remover
  ([`edf90c8`](https://github.com/dimanu-py/social-network/commit/edf90c8950bf6fe71ee32477bb6cfa90d8213c8a))

- **user**: Modify removal endpoint to search user by id instead of by username
  ([`2919a35`](https://github.com/dimanu-py/social-network/commit/2919a35b646b15cacdc0352cea890348b2342e2f))

- **user**: Call validate method in value objects after attribute assignment to use self._value and
  do not need to pass value constantly
  ([`5dfed0e`](https://github.com/dimanu-py/social-network/commit/5dfed0e18e9798ca5687a6e75b601dd352fe611e))

- **shared**: Call validate method in value objects after attribute assignment to use self._value
  and do not need to pass value constantly
  ([`1f10ded`](https://github.com/dimanu-py/social-network/commit/1f10ded759cb3d7ead1ea98fb573c0b690c647c3))

- **user**: Modify exceptions to use new domain error implementation
  ([`addd652`](https://github.com/dimanu-py/social-network/commit/addd652762bb0afee15879ac752a746499066034))

- **shared**: Modify exceptions to use new domain error implementation
  ([`1925915`](https://github.com/dimanu-py/social-network/commit/19259150ab14c420910849136d3df141fc4ab471))

- **shared**: Make domain error class received the message and type in constructor so its the only
  thing needed to defined in subclasses
  ([`e48cc3d`](https://github.com/dimanu-py/social-network/commit/e48cc3daf86e49dbc30fcb780ab279d9b50e4bcd))

- **user**: Rename to_dict method to to_primitives to just be explicit that returns primitives, not
  a dict
  ([`b6f719d`](https://github.com/dimanu-py/social-network/commit/b6f719d635f0d8235769ecea289d32a16867eefa))

- **shared**: Rename to_dict method to to_primitives to just be explicit that returns primitives,
  not a dict
  ([`8420f24`](https://github.com/dimanu-py/social-network/commit/8420f24b97e6401a1cbe96e11734b4bf37fbe8e3))

- **shared**: Use Self type hint instead of "Object"
  ([`a683ae7`](https://github.com/dimanu-py/social-network/commit/a683ae7f11905d3173f2f9a1d90edf1fd92f3afd))

- **user**: Use Self type hint instead of "Object"
  ([`365cc0f`](https://github.com/dimanu-py/social-network/commit/365cc0f171769ff315363298a8ae6eb606bd2104))

- **user**: Delete users based on username instead of id
  ([`4f4f879`](https://github.com/dimanu-py/social-network/commit/4f4f87971938597a6c0c5c81bc124beaab23f20a))

- **user**: Move empty response constant to UserModuleAcceptanceTestConfig
  ([`6976e8c`](https://github.com/dimanu-py/social-network/commit/6976e8cf1334a63e7f269e50062a8232ad53aa4b))

- **user**: Rename to_dict method from User aggregate to to_primitives
  ([`f5e9f97`](https://github.com/dimanu-py/social-network/commit/f5e9f97998cbf0611a10b20381e513e87825acd9))

- **user**: Move endpoints to infra layer instead of having them on delivery
  ([`df10d2e`](https://github.com/dimanu-py/social-network/commit/df10d2ecb3e03ebef66f4b9cf7088286c842ffd4))


## v0.5.1 (2025-03-27)

### ♻️ Refactoring

- **user**: Rename UserMother create factory method to from_signup_command and pass the command
  instead of a dict
  ([`004ff10`](https://github.com/dimanu-py/social-network/commit/004ff1081092e0d45ed00d1c1457f1a9b83d3003))

- **user**: Modify how create method in RegisterUserCommandMother is used passing a kwargs instead
  of a dict
  ([`59de101`](https://github.com/dimanu-py/social-network/commit/59de101d6ba935de560760b332e9d7009924597d))

- **user**: Convert all object mothers classmethods into staticmethods
  ([`70442f6`](https://github.com/dimanu-py/social-network/commit/70442f653eaf1fe0d98277810e6e37fe7aca1259))


## v0.5.0 (2025-02-24)

### ✨ Features

- **shared**: Add logic to allow building queries with contains
  ([`31341d8`](https://github.com/dimanu-py/social-network/commit/31341d839737dae4b88a9c1e6d3bc7b2c8802a44))

- **shared**: Add logic to allow building queries with not equal
  ([`bce0ebd`](https://github.com/dimanu-py/social-network/commit/bce0ebd507a4826d9a578c6708c5701d1e6a5f1b))

### 🪲 Bug Fixes

- **user**: Correct criteria object for integration test
  ([`2b1c4c2`](https://github.com/dimanu-py/social-network/commit/2b1c4c2f7f98941e65d310961912ca21a8286a84))

### ♻️ Refactoring

- **shared**: Clean up convert method extracting common variables outside conditionals and
  encapsulating condition generation in a helper method
  ([`45c2e51`](https://github.com/dimanu-py/social-network/commit/45c2e51b2da65ed18be1c59864a3a88782e35590))

- **shared**: Extract variable to understand better where query
  ([`46cda5d`](https://github.com/dimanu-py/social-network/commit/46cda5d8632aaf559fd283e1af15df65368acda4))

- **user**: Extract setup_method to reuse converter object
  ([`3de6fc8`](https://github.com/dimanu-py/social-network/commit/3de6fc888c9722f7a6731ced16d2eb8d98b8515f))

- **user**: Extract setup_method to reuse repository instance
  ([`6abc9a0`](https://github.com/dimanu-py/social-network/commit/6abc9a02fd1e0808da07c229400119f9c0e3a627))

- **user**: Move routers to delivery context
  ([`31977bd`](https://github.com/dimanu-py/social-network/commit/31977bdb332caebd8dedc6c646adab60391588cd))

- **user**: Generate acceptance test data inside helper method when_a_post_request_is_sent_to
  ([`60c5e12`](https://github.com/dimanu-py/social-network/commit/60c5e1293fb948e48841c4696b71b61f6fdee217))

- **user**: Clean up acceptance test using UserModuleAcceptanceTestConfig
  ([`f9dcba1`](https://github.com/dimanu-py/social-network/commit/f9dcba1f22aaab89018dd3f9a401ab8726eae0d7))

- **user**: Clean up unit test using UserModuleUnitTestConfig
  ([`917dd62`](https://github.com/dimanu-py/social-network/commit/917dd62c38204c17b2c4154592091aa9f73d9106))

- **user**: Add type hint to should_not_match mock repository
  ([`ec74ca0`](https://github.com/dimanu-py/social-network/commit/ec74ca0e3feee082a0abb4a4bf72042224fc836c))

- **user**: Rename search method to find
  ([`c5c2b33`](https://github.com/dimanu-py/social-network/commit/c5c2b3339521f2f22580deb505962e6d615de68b))


## v0.4.0 (2025-02-22)

### ✨ Features

- **user**: Create user search response object
  ([`0d165f2`](https://github.com/dimanu-py/social-network/commit/0d165f2b7c5077f832cfde48760925be9b34d8e5))

- **shared**: Implement logic to generate a where equality clause in converter
  ([`da2833e`](https://github.com/dimanu-py/social-network/commit/da2833edc9df34841a96ae5ea2f97e04f313cafa))

- **shared**: Add is_empty method to criteria to know if it has filters or not
  ([`0205b14`](https://github.com/dimanu-py/social-network/commit/0205b14ace6e9c03f0ef3b28eda05bcb0a822b97))

- **shared**: Implement basic select query with no filters
  ([`b9da488`](https://github.com/dimanu-py/social-network/commit/b9da48816a040ed5dbfcc3b1ffa1bae842aba735))

- **user**: Design how I want matching method to work in SQL
  ([`a408dda`](https://github.com/dimanu-py/social-network/commit/a408dda04bff4ad396218cde4b21e109b73c1215))

- **user**: Add username property to User
  ([`9a701ff`](https://github.com/dimanu-py/social-network/commit/9a701ff57527a7a49f9e4e59ec1a1e935cd99843))

- **user**: Define matching method in UserRepository
  ([`46aeb76`](https://github.com/dimanu-py/social-network/commit/46aeb76c4f0d67fd742ae99f6e6a4e26a9e79842))

- **user**: Design interaction with repository and criteria inside the use case
  ([`400fd7a`](https://github.com/dimanu-py/social-network/commit/400fd7acb6f4cc39fc701ec4ac28d30357886f38))

- **user**: Create Criteria object
  ([`d27bc84`](https://github.com/dimanu-py/social-network/commit/d27bc84cad580672733cfae6dd045efa2215cb89))

- **user**: Wrap Filter collection inside Filters object
  ([`6154f45`](https://github.com/dimanu-py/social-network/commit/6154f45d0ec32339310fa1eeb8787a86b16a7909))

- **user**: Create Filter object to group the combination of field, value and operator
  ([`caaa84e`](https://github.com/dimanu-py/social-network/commit/caaa84eb531b36384b76635bc1cf87e78e2e5c35))

- **user**: Create FilterOperator enum to store all possible operations
  ([`5b4e926`](https://github.com/dimanu-py/social-network/commit/5b4e9262260b8e633105a37e5fe9554bf654cabc))

- **user**: Create FilterValue object to store the value the client will search
  ([`c0d2ef4`](https://github.com/dimanu-py/social-network/commit/c0d2ef40315e6b76b6af210182e56214d9d4a452))

- **user**: Create FilterField to store the field the user will be searched by
  ([`e8a9d38`](https://github.com/dimanu-py/social-network/commit/e8a9d38079c84ed5071f8755332671be2971528f))

- **user**: Create SearchUserQuery to store query parameters
  ([`570dc26`](https://github.com/dimanu-py/social-network/commit/570dc26a0659629aa0a305f48dbb16436766199b))

- **user**: Create UserSearcher use case
  ([`c1d25df`](https://github.com/dimanu-py/social-network/commit/c1d25df9c8532bc07410c9775f9fa72bb1592ca8))

- **user**: Design interaction between router and use case
  ([`2e4b3a3`](https://github.com/dimanu-py/social-network/commit/2e4b3a330d6c80e66f01943105db9c9d2b22d9bb))

### ♻️ Refactoring

- **user**: Work with UserSearchResponse in HttpResponse
  ([`9d7362d`](https://github.com/dimanu-py/social-network/commit/9d7362dac158c5f48abeed934d11d0c7519ac33f))

- **user**: Avoid iterating again over searched_users list as UserRepository already returns them as
  a list of aggregates
  ([`bc6db59`](https://github.com/dimanu-py/social-network/commit/bc6db59a18f59db0dc346bd2a4972977abf95342))

- **shared**: Move stringify method to test class as it's only needed to be able to compare string
  queries and sqlalchemy does not process raw strings
  ([`2990dc7`](https://github.com/dimanu-py/social-network/commit/2990dc7c950b7e6c2ae5c2dd05c6e083c6dd99ba))

- **shared**: Extract common method to compile query into string for criteria converter
  ([`0fb5417`](https://github.com/dimanu-py/social-network/commit/0fb54177907ac30c019899eb4a17bbb825445b51))

- **shared**: Early return when criteria is empty
  ([`716a129`](https://github.com/dimanu-py/social-network/commit/716a129a994cf0e28b031dc4b55a930f9adc4dac))

- **user**: Rename test variable to express that what is returned is a collection of users
  ([`06203a0`](https://github.com/dimanu-py/social-network/commit/06203a03a2b8fb1be7b40d6e922691e9be227573))

- **user**: Return empty list when no user is found instead of None
  ([`a0f81ea`](https://github.com/dimanu-py/social-network/commit/a0f81ea1bc18eba41cbd0b3bf84ccd3999f76c44))

- **user**: Rename User field attributes to make them protected
  ([`5f7c76f`](https://github.com/dimanu-py/social-network/commit/5f7c76f1d802489f2a441fd93cadb20c51153af8))

- **user**: Allow UserMother to be created with fixed values passing a dictionary instead of
  coupling it to a command
  ([`7aa9522`](https://github.com/dimanu-py/social-network/commit/7aa95225f36b4b8a8c6a4815a01433c7932a0724))

- **user**: Add to_dict method to UserSignupCommand
  ([`6069f2a`](https://github.com/dimanu-py/social-network/commit/6069f2a7ad9bcde287c94585f00abeddb6e822e3))


## v0.3.0 (2025-02-18)

### ✨ Features

- **http**: Create POST request example to try application manually
  ([`15e0f42`](https://github.com/dimanu-py/social-network/commit/15e0f42098f6fcb2a29f0248e2a572083fb2aced))

- **api**: Implement lifespan to manage migration event on startup
  ([`8cd71bd`](https://github.com/dimanu-py/social-network/commit/8cd71bd82a5d5487c46815ec497c8c435d1d2205))

- **api**: Create class to be able to perform migrations on startup
  ([`de1cf53`](https://github.com/dimanu-py/social-network/commit/de1cf531f48b58900622452c3978e3e9428ad8a5))

- **migrations**: Create first migration that creates user table
  ([`10ace01`](https://github.com/dimanu-py/social-network/commit/10ace013fa9d04e47585030c7e659cba95a5dfa9))

- **migrations**: Override sqlalchemy.url variable with custom url using Settings class
  ([`22dd413`](https://github.com/dimanu-py/social-network/commit/22dd413d263e45b46bbfc89e998eedfb7f5623dd))

- **migrations**: Add project Base metadata in alembic environment
  ([`6186174`](https://github.com/dimanu-py/social-network/commit/61861741fd4adb73566053039e55caad02d8642f))

- **migrations**: Enable ruff to format and lint revisions scripts
  ([`a342180`](https://github.com/dimanu-py/social-network/commit/a34218051b90ba408007aaf167adb2a282a2300c))

- **migrations**: Specify a time format for revision files so they appear ordered
  ([`cd0d3ea`](https://github.com/dimanu-py/social-network/commit/cd0d3ea52591f4609e2c18a2ca1319a7a7f4b8cf))

- **migrations**: Initialize alembic environment to manage migrations
  ([`ec0dff1`](https://github.com/dimanu-py/social-network/commit/ec0dff149aedf242ba007462c436c5a00cc7c0c5))

### 🪲 Bug Fixes

- **migrations**: Import all sqlalchemy models so alembic detects correctly changes
  ([`8cf5141`](https://github.com/dimanu-py/social-network/commit/8cf5141d20017464b0412a013e8abcc1c234bcdf))

### ♻️ Refactoring

- **user**: Remove the use of the logger inside endpoint and pass resource to logged when request is
  successful
  ([`abdfce3`](https://github.com/dimanu-py/social-network/commit/abdfce3e2f51bed90a6a0ab81ecc1fe3ff12bd50))

- **api**: Pass exception when internal server error is raised so it can be logged
  ([`a0fb087`](https://github.com/dimanu-py/social-network/commit/a0fb0878856e1e9da9324064bf16b3dcba6691c7))

- **shared**: Log error and request information inside HttpResponse class
  ([`13db580`](https://github.com/dimanu-py/social-network/commit/13db58001a4b517c85bf99ee4edd8f572a677d81))

- **user**: Use context manager to be able to perform startup event on acceptance test
  ([`9fa2ad5`](https://github.com/dimanu-py/social-network/commit/9fa2ad53e921083193d512d49bb75450c71146a8))

- **user**: Remove table creation from engine_generator and encapsulate it between a try-finally
  clause
  ([`26f7670`](https://github.com/dimanu-py/social-network/commit/26f7670b68fdec30f0b953e1329f9a51b3b8caf0))

- **user**: Write correct type hint for engine_generator
  ([`ded9d3b`](https://github.com/dimanu-py/social-network/commit/ded9d3b46e6f50986d68c3fe2768f46e886a5ab9))


## v0.2.0 (2025-02-11)

### ✨ Features

- **user**: Log when a request to user signup gets processed correctly
  ([`6d414db`](https://github.com/dimanu-py/social-network/commit/6d414db7c82daeb1f54596f50f5101550a8b0583))

- **user**: Log when a domain error is raised
  ([`08a5ed2`](https://github.com/dimanu-py/social-network/commit/08a5ed2a2f48b2edb676b899ed05ff3758c5fd20))

- **user**: Log requests received to sign up user route
  ([`3ebc796`](https://github.com/dimanu-py/social-network/commit/3ebc7963c7465f62be5683419fa417b1c02da569))

- **shared**: Implement logic to create a logger with two handlers for dev and production
  ([`74a73e9`](https://github.com/dimanu-py/social-network/commit/74a73e9e7e62220803d918722aa4db0b90175903))

- **shared**: Add custom log formatter
  ([`55d679a`](https://github.com/dimanu-py/social-network/commit/55d679a708c8d8d4abf95259d02242a3e4d16413))

- **app**: Add custom handler to catch unexpected exceptions
  ([`3d2e6c6`](https://github.com/dimanu-py/social-network/commit/3d2e6c6b85e8ac5082d089e0a57634593d4a2826))

- **user**: Wrap use case call within try-except block and handle domain errors
  ([`933e7dc`](https://github.com/dimanu-py/social-network/commit/933e7dc3adc582148eaeedbc181eb488851aacb8))

### ♻️ Refactoring

- **shared**: Forced log folder to be at the root of the project
  ([`268f7cb`](https://github.com/dimanu-py/social-network/commit/268f7cbc0649d378c400a677e8d33ea693dd07c3))

- **shared**: Rename http response module file
  ([`ce3bd86`](https://github.com/dimanu-py/social-network/commit/ce3bd86ecfec380a7074f8531978b08a25ca6eb5))

- **shared**: Move modules related to http to specific package
  ([`b442f16`](https://github.com/dimanu-py/social-network/commit/b442f16ed8c7eb7efecd65b52fd190e653768532))

- **user**: Let test method receive the request in the call
  ([`9e98923`](https://github.com/dimanu-py/social-network/commit/9e989236e2b59dbca88a2285f552c0c220ee58e1))


## v0.1.0 (2025-02-11)

### ✨ Features

- **user**: Add id property to User to avoid direct accessing its attributes
  ([`2a224fe`](https://github.com/dimanu-py/social-network/commit/2a224febdc281ba8d61999c33265708f93985aae))

- **user**: Add to_aggregate method to UserModel to be able to convert database data into domain
  model
  ([`e339da3`](https://github.com/dimanu-py/social-network/commit/e339da39cee83c1321608198d911b071e5877dd0))

- **user**: Implement search method in PostgresUserRepository
  ([`76099de`](https://github.com/dimanu-py/social-network/commit/76099dec3e414b2c080332e8e59ad4261edb0317))

- **user**: Add search abstractmethod to UserRepository
  ([`89ece4b`](https://github.com/dimanu-py/social-network/commit/89ece4b6844df7c2da5b0c372f43cdd01fe386bb))

- **user**: Concrete implementation of UserRepository using Postgres
  ([`5006d91`](https://github.com/dimanu-py/social-network/commit/5006d91853313a17f37f7528d2cbeb4c861add77))

### 🪲 Bug Fixes

- **shared**: Specify in database url that asyncpg must be used instead of pyscopg
  ([`dbda488`](https://github.com/dimanu-py/social-network/commit/dbda488d8476d40ae5d6ab4f02bf65fefe466b06))

### ♻️ Refactoring

- **user**: Extract async engine generation to function and injected into router
  ([`d8c6cf9`](https://github.com/dimanu-py/social-network/commit/d8c6cf9f03196c8516f7b6f04217c4872b346a8a))

- **user**: Create async fixture to yield an engine and be able to create and delete tables on every
  test
  ([`5bc34fe`](https://github.com/dimanu-py/social-network/commit/5bc34fe7834ba28293a172d830adab0e0ae544d9))

- **user**: Remove the use of SessionMaker and pass directly an AsyncEngine
  ([`f0d1e75`](https://github.com/dimanu-py/social-network/commit/f0d1e75deb8068c2d82838f46dfd1dfa7a906157))

- **shared**: Create async engines and sessions with SQLAlchemy instead of working with synchronous
  operations
  ([`7e9c431`](https://github.com/dimanu-py/social-network/commit/7e9c4318c551255fa0f1e545d5141e41407efa34))

- **user**: Extract semantic methods in acceptance test
  ([`0468939`](https://github.com/dimanu-py/social-network/commit/04689395446bb7bc813820fc0912a30a748f019b))

- **user**: Remove unused InMemoryUserRepository
  ([`fc16017`](https://github.com/dimanu-py/social-network/commit/fc16017b38ea859377c0d58aa4a43d0b6e2bbd9c))

- **user**: Use PostgresUserRepository inside router instead of in memory
  ([`a5edc25`](https://github.com/dimanu-py/social-network/commit/a5edc25ad83bd5d4d26140fca9ca0cdaf0a2e58c))
