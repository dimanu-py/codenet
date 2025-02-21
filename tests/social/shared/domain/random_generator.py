from faker import Faker


class RandomGenerator:
    faker = Faker()

    @classmethod
    def uuid(cls) -> str:
        return str(cls.faker.uuid4())

    @classmethod
    def name(cls) -> str:
        return cls.faker.name()

    @classmethod
    def username(cls) -> str:
        return cls.faker.user_name()

    @classmethod
    def email(cls) -> str:
        return cls.faker.email()

    @classmethod
    def word(cls) -> str:
        return cls.faker.word()
