from abc import ABC

from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class ErrorResponse(ABC, BaseModel):
    status_code: int
    detail: dict

    def as_json(self) -> JSONResponse:
        return JSONResponse(
            content={"detail": self.detail},
            status_code=self.status_code,
        )

    def __str__(self) -> str:
        return f"{self.detail}"


class UnprocessableEntityError(ErrorResponse):
    status_code: int = Field(default=status.HTTP_422_UNPROCESSABLE_CONTENT)
    detail: dict = Field(default={"message": "Unprocessable Entity"})


class ResourceNotFoundError(ErrorResponse):
    status_code: int = Field(default=status.HTTP_404_NOT_FOUND)
    detail: dict = Field(default={"message": "Not Found"})


class InternalServerError(ErrorResponse):
    status_code: int = Field(default=status.HTTP_500_INTERNAL_SERVER_ERROR)
    detail: dict = Field(default={"message": "An unexpected error occurred."})
