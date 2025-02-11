from fastapi.responses import JSONResponse

from src.shared.domain.exceptions.domain_error import DomainError
from src.shared.infra.http.status_code import StatusCode


class HttpResponse:
    @staticmethod
    def domain_error(error: DomainError, status_code: StatusCode) -> JSONResponse:
        return JSONResponse(content={"error": error.to_dict()}, status_code=status_code)

    @staticmethod
    def internal_error() -> JSONResponse:
        return JSONResponse(
            content={"error": "Internal server error"},
            status_code=StatusCode.INTERNAL_SERVER_ERROR,
        )

    @staticmethod
    def created() -> JSONResponse:
        return JSONResponse(content={}, status_code=StatusCode.CREATED)

    @staticmethod
    def ok(content: dict) -> JSONResponse:
        return JSONResponse(content=content, status_code=StatusCode.OK)
