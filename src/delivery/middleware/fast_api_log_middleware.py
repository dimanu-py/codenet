import time

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from src.shared.infra.logger.fastapi_file_logger import FastApiFileLogger, SuccessRecordDetails, ErrorRecordDetails


class FastapiLogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, logger: FastApiFileLogger) -> None:
        super().__init__(app)
        self._logger = logger

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time

        if response.status_code < 400:
            self._logger.success(
                message=request.url.path,
                details=SuccessRecordDetails(
                    method=request.method,
                    source=request.url.path,
                    process_time=process_time,
                    status_code=response.status_code,
                ),
            )
        else:
            self._logger.error(
                message=request.url.path,
                details=ErrorRecordDetails(
                    method=request.method,
                    error_message=str(response),
                    source=request.url.path,
                    status_code=response.status_code,
                ),
            )

        return response
