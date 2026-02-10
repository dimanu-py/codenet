import uuid

from src.shared.domain.uuid_generator import UuidGenerator


class NativeUuidGenerator(UuidGenerator):
    @classmethod
    def random(cls) -> str:
        return str(uuid.uuid4())