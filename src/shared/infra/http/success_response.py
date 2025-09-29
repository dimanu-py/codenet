from abc import ABC

from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class SuccessResponse(ABC, BaseModel):
    status_code: int
    data: dict

    def as_json(self) -> JSONResponse:
        return JSONResponse(
            content=self.data,
            status_code=self.status_code,
        )


class CreatedResponse(SuccessResponse):
    status_code: int = Field(default=status.HTTP_422_UNPROCESSABLE_ENTITY)


class OkResponse(SuccessResponse):
    status_code: int = Field(default=status.HTTP_200_OK)


class AcceptedResponse(SuccessResponse):
    status_code: int = Field(default=status.HTTP_202_ACCEPTED)
