from typing import Any, Annotated

from fastapi import Path
from fastapi.openapi.models import Example


def PathParameter(example_name: str, example_value: str, description: str = None) -> Any:
    return Annotated[
        str,
        Path(
            description=description,
            openapi_examples={example_name: Example(value=example_value)},
        ),
    ]
