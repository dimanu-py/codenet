from faker import Faker


class RandomGenerator:
    faker = Faker()

    @classmethod
    def uuid(cls) -> str:
        return str(cls.faker.uuid4())
