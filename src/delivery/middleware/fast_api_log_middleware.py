import time

from fastapi import Request, Response, FastAPI
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.shared.infra.logger.fastapi_file_logger import FastApiFileLogger


class FastapiLogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, logger: FastApiFileLogger) -> None:
        super().__init__(app)
        self._logger = logger

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time

        if response.status_code < 400:
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
