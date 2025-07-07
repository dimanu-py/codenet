from fastapi.responses import JSONResponse

from src.shared.domain.exceptions.domain_error import DomainError
from src.shared.infra.http.status_code import StatusCode
from src.shared.infra.log.logger import create_logger

user_logger = create_logger("user")


class HttpResponse:
    @staticmethod
    def domain_error(error: DomainError, status_code: StatusCode) -> JSONResponse:
        user_logger.error(
            "error - domain error",
            extra={
                "extra": {"error": error.to_primitives(), "status_code": status_code}
            },
        )
        return JSONResponse(
            content={"error": error.to_primitives()}, status_code=status_code
        )

    @staticmethod
    def internal_error(error: Exception) -> JSONResponse:
        user_logger.error(
            "error - internal server error",
            extra={
                "extra": {"error": str(error)},
                "status_code": StatusCode.INTERNAL_SERVER_ERROR,
            },
        )
        return JSONResponse(
            content={"error": "Internal server error"},
            status_code=StatusCode.INTERNAL_SERVER_ERROR,
        )

    @staticmethod
    def created(resource: str) -> JSONResponse:
        user_logger.info(
            f"resource - {resource}",
            extra={"extra": {"status_code": StatusCode.CREATED}},
        )
        return JSONResponse(content={}, status_code=StatusCode.CREATED)

    @staticmethod
    def ok(content: dict) -> JSONResponse:
        return JSONResponse(content=content, status_code=StatusCode.OK)
