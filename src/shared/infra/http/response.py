from abc import abstractmethod, ABC
from typing import Any

from pydantic import BaseModel
from fastapi.responses import JSONResponse


class HttpResponse(ABC, BaseModel):
    status_code: int

    @abstractmethod
    def as_json(self) -> JSONResponse:
        raise NotImplementedError

    def model_dump(self, **kwargs: Any) -> dict[str, Any]:
        kwargs.setdefault("exclude_none", True)
        return super().model_dump(**kwargs)

    def model_dump_json(self, **kwargs: Any) -> str:
        kwargs.setdefault("exclude_none", True)
        return super().model_dump_json(**kwargs)


class SuccessResponse(HttpResponse):
    data: dict

    def as_json(self) -> JSONResponse:
        return JSONResponse(
            content=self.data,
            status_code=self.status_code,
        )


class ErrorResponse(HttpResponse):
    detail: str

    def as_json(self) -> JSONResponse:
        return JSONResponse(
            content={"detail": self.detail},
            status_code=self.status_code,
        )
