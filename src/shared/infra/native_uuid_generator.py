import uuid
from typing import override

from src.shared.domain.uuid_generator import UuidGenerator


class NativeUuidGenerator(UuidGenerator):
    @override
    def random(self) -> str:
        return str(uuid.uuid4())
