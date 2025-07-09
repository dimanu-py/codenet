# CHANGELOG

<!-- version list -->

## v1.0.0 (2025-07-09)

### Bug Fixes

- Correct mypy errors
  ([`5a41e26`](https://github.com/dimanu-py/codenet/commit/5a41e26e6312359f1d566ff13508a73cc0b6aadf))

- **user**: Add missing imports to removal endpoint
  ([`402ab4b`](https://github.com/dimanu-py/codenet/commit/402ab4b328fbc3b1b144d163541e187c1d8db706))

- **user**: Modify 'should_find' method of mock repository to only compare user id and return a full
  user
  ([`2e6dbcc`](https://github.com/dimanu-py/codenet/commit/2e6dbcc27f24ae52017d6a288fe37a58aec2c760))

- **user**: Modify 'should_remove' method of mock repository to only compare user id
  ([`b1fc4ab`](https://github.com/dimanu-py/codenet/commit/b1fc4ab3fd5ed7580493de660074c09e1050bf32))

- **user**: Update user removal logic to use UserId to delete from database
  ([`5a4a127`](https://github.com/dimanu-py/codenet/commit/5a4a1273bb08fdea9313b6f33acdcb7c412e0eab))

- **user**: Verify removal router returns 200 instead of 202
  ([`98765e0`](https://github.com/dimanu-py/codenet/commit/98765e0a2c60bbc157f5c79f0c5481c893acc929))

### Features

- **delivery**: Include removal router in application
  ([`38cfd53`](https://github.com/dimanu-py/codenet/commit/38cfd530d4d47d13173bf739237d4b4885a8cdc4))

- **user**: Add 'delete' signature method to UserRepository interface
  ([`db39d5a`](https://github.com/dimanu-py/codenet/commit/db39d5a89a0ea55e9e04dc606dc90950bcf1a8ff))

- **user**: Create base router for all users endpoints
  ([`334e305`](https://github.com/dimanu-py/codenet/commit/334e3054d305d38de289405509167217e1192d5d))

- **user**: Create UserRemover use case
  ([`65cff03`](https://github.com/dimanu-py/codenet/commit/65cff0348c50408ba821edf3a9c3723634eae10f))

- **user**: Define how removal endpoint will orchestrate operations to remove user
  ([`3ef534f`](https://github.com/dimanu-py/codenet/commit/3ef534f5e84dab9297e05e930c1a6034cdbad9f9))

- **user**: Design how user remover use case deletes existing user
  ([`b11bf70`](https://github.com/dimanu-py/codenet/commit/b11bf7038c86264ff7e3661f77ca2112b22ce81b))

- **user**: Implement 'delete' method in PostgresUserRepository
  ([`0da5cb9`](https://github.com/dimanu-py/codenet/commit/0da5cb9d39bad2d70f653ef2b0f215d7bac99b3b))

- **user**: Implement UserNotFoundError domain error
  ([`0dc3a8b`](https://github.com/dimanu-py/codenet/commit/0dc3a8be27b64929814877d5ad4ad91f7af4e2ae))

- **user**: Implement UserRemovalCommand dto
  ([`19bb9d7`](https://github.com/dimanu-py/codenet/commit/19bb9d7d3b52786efe01c214d3671fdbc2d229b8))

- **user**: Import implemented classes in removal user and return empty dict if successful
  ([`5039282`](https://github.com/dimanu-py/codenet/commit/50392820bdae75fc3728368dd3098703df1a0605))

### Refactoring

- **delivery**: Include user routes instead of all routers one by one
  ([`033963e`](https://github.com/dimanu-py/codenet/commit/033963ea16d8e4c8e068695117f8160de5143405))

- **shared**: Call validate method in value objects after attribute assignment to use self._value
  and do not need to pass value constantly
  ([`1f10ded`](https://github.com/dimanu-py/codenet/commit/1f10ded759cb3d7ead1ea98fb573c0b690c647c3))

- **shared**: Make domain error class received the message and type in constructor so its the only
  thing needed to defined in subclasses
  ([`e48cc3d`](https://github.com/dimanu-py/codenet/commit/e48cc3daf86e49dbc30fcb780ab279d9b50e4bcd))

- **shared**: Modify exceptions to use new domain error implementation
  ([`1925915`](https://github.com/dimanu-py/codenet/commit/19259150ab14c420910849136d3df141fc4ab471))

- **shared**: Rename to_dict method to to_primitives to just be explicit that returns primitives,
  not a dict
  ([`8420f24`](https://github.com/dimanu-py/codenet/commit/8420f24b97e6401a1cbe96e11734b4bf37fbe8e3))

- **shared**: Use Self type hint instead of "Object"
  ([`a683ae7`](https://github.com/dimanu-py/codenet/commit/a683ae7f11905d3173f2f9a1d90edf1fd92f3afd))

- **user**: Call validate method in value objects after attribute assignment to use self._value and
  do not need to pass value constantly
  ([`5dfed0e`](https://github.com/dimanu-py/codenet/commit/5dfed0e18e9798ca5687a6e75b601dd352fe611e))

- **user**: Delete users based on username instead of id
  ([`4f4f879`](https://github.com/dimanu-py/codenet/commit/4f4f87971938597a6c0c5c81bc124beaab23f20a))

- **user**: Modify exceptions to use new domain error implementation
  ([`addd652`](https://github.com/dimanu-py/codenet/commit/addd652762bb0afee15879ac752a746499066034))

- **user**: Modify removal endpoint to search user by id instead of by username
  ([`2919a35`](https://github.com/dimanu-py/codenet/commit/2919a35b646b15cacdc0352cea890348b2342e2f))

- **user**: Move empty response constant to UserModuleAcceptanceTestConfig
  ([`6976e8c`](https://github.com/dimanu-py/codenet/commit/6976e8cf1334a63e7f269e50062a8232ad53aa4b))

- **user**: Move endpoints to infra layer instead of having them on delivery
  ([`df10d2e`](https://github.com/dimanu-py/codenet/commit/df10d2ecb3e03ebef66f4b9cf7088286c842ffd4))

- **user**: Rename to_dict method from User aggregate to to_primitives
  ([`f5e9f97`](https://github.com/dimanu-py/codenet/commit/f5e9f97998cbf0611a10b20381e513e87825acd9))

- **user**: Rename to_dict method to to_primitives to just be explicit that returns primitives, not
  a dict
  ([`b6f719d`](https://github.com/dimanu-py/codenet/commit/b6f719d635f0d8235769ecea289d32a16867eefa))

- **user**: Rename use case from user removal to user remover
  ([`edf90c8`](https://github.com/dimanu-py/codenet/commit/edf90c8950bf6fe71ee32477bb6cfa90d8213c8a))

- **user**: Use Self type hint instead of "Object"
  ([`365cc0f`](https://github.com/dimanu-py/codenet/commit/365cc0f171769ff315363298a8ae6eb606bd2104))


## v0.5.1 (2025-03-27)

### Refactoring

- **user**: Convert all object mothers classmethods into staticmethods
  ([`70442f6`](https://github.com/dimanu-py/codenet/commit/70442f653eaf1fe0d98277810e6e37fe7aca1259))

- **user**: Modify how create method in RegisterUserCommandMother is used passing a kwargs instead
  of a dict
  ([`59de101`](https://github.com/dimanu-py/codenet/commit/59de101d6ba935de560760b332e9d7009924597d))

- **user**: Rename UserMother create factory method to from_signup_command and pass the command
  instead of a dict
  ([`004ff10`](https://github.com/dimanu-py/codenet/commit/004ff1081092e0d45ed00d1c1457f1a9b83d3003))


## v0.5.0 (2025-02-24)

### Bug Fixes

- **user**: Correct criteria object for integration test
  ([`2b1c4c2`](https://github.com/dimanu-py/codenet/commit/2b1c4c2f7f98941e65d310961912ca21a8286a84))

### Features

- **shared**: Add logic to allow building queries with contains
  ([`31341d8`](https://github.com/dimanu-py/codenet/commit/31341d839737dae4b88a9c1e6d3bc7b2c8802a44))

- **shared**: Add logic to allow building queries with not equal
  ([`bce0ebd`](https://github.com/dimanu-py/codenet/commit/bce0ebd507a4826d9a578c6708c5701d1e6a5f1b))

### Refactoring

- **shared**: Clean up convert method extracting common variables outside conditionals and
  encapsulating condition generation in a helper method
  ([`45c2e51`](https://github.com/dimanu-py/codenet/commit/45c2e51b2da65ed18be1c59864a3a88782e35590))

- **shared**: Extract variable to understand better where query
  ([`46cda5d`](https://github.com/dimanu-py/codenet/commit/46cda5d8632aaf559fd283e1af15df65368acda4))

- **user**: Add type hint to should_not_match mock repository
  ([`ec74ca0`](https://github.com/dimanu-py/codenet/commit/ec74ca0e3feee082a0abb4a4bf72042224fc836c))

- **user**: Clean up acceptance test using UserModuleAcceptanceTestConfig
  ([`f9dcba1`](https://github.com/dimanu-py/codenet/commit/f9dcba1f22aaab89018dd3f9a401ab8726eae0d7))

- **user**: Clean up unit test using UserModuleUnitTestConfig
  ([`917dd62`](https://github.com/dimanu-py/codenet/commit/917dd62c38204c17b2c4154592091aa9f73d9106))

- **user**: Extract setup_method to reuse converter object
  ([`3de6fc8`](https://github.com/dimanu-py/codenet/commit/3de6fc888c9722f7a6731ced16d2eb8d98b8515f))

- **user**: Extract setup_method to reuse repository instance
  ([`6abc9a0`](https://github.com/dimanu-py/codenet/commit/6abc9a02fd1e0808da07c229400119f9c0e3a627))

- **user**: Generate acceptance test data inside helper method when_a_post_request_is_sent_to
  ([`60c5e12`](https://github.com/dimanu-py/codenet/commit/60c5e1293fb948e48841c4696b71b61f6fdee217))

- **user**: Move routers to delivery context
  ([`31977bd`](https://github.com/dimanu-py/codenet/commit/31977bdb332caebd8dedc6c646adab60391588cd))

- **user**: Rename search method to find
  ([`c5c2b33`](https://github.com/dimanu-py/codenet/commit/c5c2b3339521f2f22580deb505962e6d615de68b))


## v0.4.0 (2025-02-22)

### Features

- **shared**: Add is_empty method to criteria to know if it has filters or not
  ([`0205b14`](https://github.com/dimanu-py/codenet/commit/0205b14ace6e9c03f0ef3b28eda05bcb0a822b97))

- **shared**: Implement basic select query with no filters
  ([`b9da488`](https://github.com/dimanu-py/codenet/commit/b9da48816a040ed5dbfcc3b1ffa1bae842aba735))

- **shared**: Implement logic to generate a where equality clause in converter
  ([`da2833e`](https://github.com/dimanu-py/codenet/commit/da2833edc9df34841a96ae5ea2f97e04f313cafa))

- **user**: Add username property to User
  ([`9a701ff`](https://github.com/dimanu-py/codenet/commit/9a701ff57527a7a49f9e4e59ec1a1e935cd99843))

- **user**: Create Criteria object
  ([`d27bc84`](https://github.com/dimanu-py/codenet/commit/d27bc84cad580672733cfae6dd045efa2215cb89))

- **user**: Create Filter object to group the combination of field, value and operator
  ([`caaa84e`](https://github.com/dimanu-py/codenet/commit/caaa84eb531b36384b76635bc1cf87e78e2e5c35))

- **user**: Create FilterField to store the field the user will be searched by
  ([`e8a9d38`](https://github.com/dimanu-py/codenet/commit/e8a9d38079c84ed5071f8755332671be2971528f))

- **user**: Create FilterOperator enum to store all possible operations
  ([`5b4e926`](https://github.com/dimanu-py/codenet/commit/5b4e9262260b8e633105a37e5fe9554bf654cabc))

- **user**: Create FilterValue object to store the value the client will search
  ([`c0d2ef4`](https://github.com/dimanu-py/codenet/commit/c0d2ef40315e6b76b6af210182e56214d9d4a452))

- **user**: Create SearchUserQuery to store query parameters
  ([`570dc26`](https://github.com/dimanu-py/codenet/commit/570dc26a0659629aa0a305f48dbb16436766199b))

- **user**: Create user search response object
  ([`0d165f2`](https://github.com/dimanu-py/codenet/commit/0d165f2b7c5077f832cfde48760925be9b34d8e5))

- **user**: Create UserSearcher use case
  ([`c1d25df`](https://github.com/dimanu-py/codenet/commit/c1d25df9c8532bc07410c9775f9fa72bb1592ca8))

- **user**: Define matching method in UserRepository
  ([`46aeb76`](https://github.com/dimanu-py/codenet/commit/46aeb76c4f0d67fd742ae99f6e6a4e26a9e79842))

- **user**: Design how I want matching method to work in SQL
  ([`a408dda`](https://github.com/dimanu-py/codenet/commit/a408dda04bff4ad396218cde4b21e109b73c1215))

- **user**: Design interaction between router and use case
  ([`2e4b3a3`](https://github.com/dimanu-py/codenet/commit/2e4b3a330d6c80e66f01943105db9c9d2b22d9bb))

- **user**: Design interaction with repository and criteria inside the use case
  ([`400fd7a`](https://github.com/dimanu-py/codenet/commit/400fd7acb6f4cc39fc701ec4ac28d30357886f38))

- **user**: Wrap Filter collection inside Filters object
  ([`6154f45`](https://github.com/dimanu-py/codenet/commit/6154f45d0ec32339310fa1eeb8787a86b16a7909))

### Refactoring

- **shared**: Early return when criteria is empty
  ([`716a129`](https://github.com/dimanu-py/codenet/commit/716a129a994cf0e28b031dc4b55a930f9adc4dac))

- **shared**: Extract common method to compile query into string for criteria converter
  ([`0fb5417`](https://github.com/dimanu-py/codenet/commit/0fb54177907ac30c019899eb4a17bbb825445b51))

- **shared**: Move stringify method to test class as it's only needed to be able to compare string
  queries and sqlalchemy does not process raw strings
  ([`2990dc7`](https://github.com/dimanu-py/codenet/commit/2990dc7c950b7e6c2ae5c2dd05c6e083c6dd99ba))

- **user**: Add to_dict method to UserSignupCommand
  ([`6069f2a`](https://github.com/dimanu-py/codenet/commit/6069f2a7ad9bcde287c94585f00abeddb6e822e3))

- **user**: Allow UserMother to be created with fixed values passing a dictionary instead of
  coupling it to a command
  ([`7aa9522`](https://github.com/dimanu-py/codenet/commit/7aa95225f36b4b8a8c6a4815a01433c7932a0724))

- **user**: Avoid iterating again over searched_users list as UserRepository already returns them as
  a list of aggregates
  ([`bc6db59`](https://github.com/dimanu-py/codenet/commit/bc6db59a18f59db0dc346bd2a4972977abf95342))

- **user**: Rename test variable to express that what is returned is a collection of users
  ([`06203a0`](https://github.com/dimanu-py/codenet/commit/06203a03a2b8fb1be7b40d6e922691e9be227573))

- **user**: Rename User field attributes to make them protected
  ([`5f7c76f`](https://github.com/dimanu-py/codenet/commit/5f7c76f1d802489f2a441fd93cadb20c51153af8))

- **user**: Return empty list when no user is found instead of None
  ([`a0f81ea`](https://github.com/dimanu-py/codenet/commit/a0f81ea1bc18eba41cbd0b3bf84ccd3999f76c44))

- **user**: Work with UserSearchResponse in HttpResponse
  ([`9d7362d`](https://github.com/dimanu-py/codenet/commit/9d7362dac158c5f48abeed934d11d0c7519ac33f))


## v0.3.0 (2025-02-18)

### Bug Fixes

- **migrations**: Import all sqlalchemy models so alembic detects correctly changes
  ([`8cf5141`](https://github.com/dimanu-py/codenet/commit/8cf5141d20017464b0412a013e8abcc1c234bcdf))

### Features

- **api**: Create class to be able to perform migrations on startup
  ([`de1cf53`](https://github.com/dimanu-py/codenet/commit/de1cf531f48b58900622452c3978e3e9428ad8a5))

- **api**: Implement lifespan to manage migration event on startup
  ([`8cd71bd`](https://github.com/dimanu-py/codenet/commit/8cd71bd82a5d5487c46815ec497c8c435d1d2205))

- **http**: Create POST request example to try application manually
  ([`15e0f42`](https://github.com/dimanu-py/codenet/commit/15e0f42098f6fcb2a29f0248e2a572083fb2aced))

- **migrations**: Add project Base metadata in alembic environment
  ([`6186174`](https://github.com/dimanu-py/codenet/commit/61861741fd4adb73566053039e55caad02d8642f))

- **migrations**: Create first migration that creates user table
  ([`10ace01`](https://github.com/dimanu-py/codenet/commit/10ace013fa9d04e47585030c7e659cba95a5dfa9))

- **migrations**: Enable ruff to format and lint revisions scripts
  ([`a342180`](https://github.com/dimanu-py/codenet/commit/a34218051b90ba408007aaf167adb2a282a2300c))

- **migrations**: Initialize alembic environment to manage migrations
  ([`ec0dff1`](https://github.com/dimanu-py/codenet/commit/ec0dff149aedf242ba007462c436c5a00cc7c0c5))

- **migrations**: Override sqlalchemy.url variable with custom url using Settings class
  ([`22dd413`](https://github.com/dimanu-py/codenet/commit/22dd413d263e45b46bbfc89e998eedfb7f5623dd))

- **migrations**: Specify a time format for revision files so they appear ordered
  ([`cd0d3ea`](https://github.com/dimanu-py/codenet/commit/cd0d3ea52591f4609e2c18a2ca1319a7a7f4b8cf))

### Refactoring

- **api**: Pass exception when internal server error is raised so it can be logged
  ([`a0fb087`](https://github.com/dimanu-py/codenet/commit/a0fb0878856e1e9da9324064bf16b3dcba6691c7))

- **shared**: Log error and request information inside HttpResponse class
  ([`13db580`](https://github.com/dimanu-py/codenet/commit/13db58001a4b517c85bf99ee4edd8f572a677d81))

- **user**: Remove table creation from engine_generator and encapsulate it between a try-finally
  clause
  ([`26f7670`](https://github.com/dimanu-py/codenet/commit/26f7670b68fdec30f0b953e1329f9a51b3b8caf0))

- **user**: Remove the use of the logger inside endpoint and pass resource to logged when request is
  successful
  ([`abdfce3`](https://github.com/dimanu-py/codenet/commit/abdfce3e2f51bed90a6a0ab81ecc1fe3ff12bd50))

- **user**: Use context manager to be able to perform startup event on acceptance test
  ([`9fa2ad5`](https://github.com/dimanu-py/codenet/commit/9fa2ad53e921083193d512d49bb75450c71146a8))

- **user**: Write correct type hint for engine_generator
  ([`ded9d3b`](https://github.com/dimanu-py/codenet/commit/ded9d3b46e6f50986d68c3fe2768f46e886a5ab9))


## v0.2.0 (2025-02-11)

### Features

- **app**: Add custom handler to catch unexpected exceptions
  ([`3d2e6c6`](https://github.com/dimanu-py/codenet/commit/3d2e6c6b85e8ac5082d089e0a57634593d4a2826))

- **shared**: Add custom log formatter
  ([`55d679a`](https://github.com/dimanu-py/codenet/commit/55d679a708c8d8d4abf95259d02242a3e4d16413))

- **shared**: Implement logic to create a logger with two handlers for dev and production
  ([`74a73e9`](https://github.com/dimanu-py/codenet/commit/74a73e9e7e62220803d918722aa4db0b90175903))

- **user**: Log requests received to sign up user route
  ([`3ebc796`](https://github.com/dimanu-py/codenet/commit/3ebc7963c7465f62be5683419fa417b1c02da569))

- **user**: Log when a domain error is raised
  ([`08a5ed2`](https://github.com/dimanu-py/codenet/commit/08a5ed2a2f48b2edb676b899ed05ff3758c5fd20))

- **user**: Log when a request to user signup gets processed correctly
  ([`6d414db`](https://github.com/dimanu-py/codenet/commit/6d414db7c82daeb1f54596f50f5101550a8b0583))

- **user**: Wrap use case call within try-except block and handle domain errors
  ([`933e7dc`](https://github.com/dimanu-py/codenet/commit/933e7dc3adc582148eaeedbc181eb488851aacb8))

### Refactoring

- **shared**: Forced log folder to be at the root of the project
  ([`268f7cb`](https://github.com/dimanu-py/codenet/commit/268f7cbc0649d378c400a677e8d33ea693dd07c3))

- **shared**: Move modules related to http to specific package
  ([`b442f16`](https://github.com/dimanu-py/codenet/commit/b442f16ed8c7eb7efecd65b52fd190e653768532))

- **shared**: Rename http response module file
  ([`ce3bd86`](https://github.com/dimanu-py/codenet/commit/ce3bd86ecfec380a7074f8531978b08a25ca6eb5))

- **user**: Let test method receive the request in the call
  ([`9e98923`](https://github.com/dimanu-py/codenet/commit/9e989236e2b59dbca88a2285f552c0c220ee58e1))


## v0.1.0 (2025-02-11)

- Initial Release
