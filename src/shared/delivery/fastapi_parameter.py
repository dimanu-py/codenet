from typing import Any, TypedDict

from fastapi import Path, Query
from fastapi.openapi.models import Example


class ApiDocExample(TypedDict):
    name: str
    value: Any


def PathParameter(examples: list[ApiDocExample], description: str | None = None) -> Any:
    return Path(
        description=description,
        openapi_examples={example["name"]: Example(value=example["value"]) for example in examples},
    )


def QueryParameter(examples: list[ApiDocExample], description: str | None = None) -> Any:
    return Query(
        description=description,
        openapi_examples={example["name"]: Example(value=example["value"]) for example in examples},
    )
