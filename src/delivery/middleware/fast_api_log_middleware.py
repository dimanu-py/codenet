import time

from fastapi import Request, Response, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.shared.domain.exceptions.domain_error import DomainError
from src.shared.infra.logger.fastapi_file_logger import FastApiFileLogger


class FastapiLogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, logger: FastApiFileLogger) -> None:
        super().__init__(app)
        self._logger = logger

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.perf_counter()

        try:
            response = await call_next(request)
            process_time = time.perf_counter() - start_time

            self._logger.info(
                message=f"success - {request.url.path}",
                details={
                    "method": request.method,
                    "source": request.url.path,
                    "process_time": process_time,
                    "status_code": response.status_code,
                },
            )

            return response

        except Exception as exc:
            process_time = time.perf_counter() - start_time
            if isinstance(exc, DomainError):
                self._logger.error(
                    message=f"domain_error - {request.url.path}",
                    details={
                        "error": exc.to_primitives(),
                        "method": request.method,
                        "path": request.url.path,
                        "process_time": process_time,
                    },
                )
            else:
                self._logger.error(
                    message=f"unexpected_error - {request.url.path}",
                    details={
                        "error": {"message": str(exc)},
                        "method": request.method,
                        "path": request.url.path,
                        "process_time": process_time,
                    },
                )

            raise
