from fastapi.responses import JSONResponse

from src.shared.infra.http.error_response import ErrorResponse
from src.shared.infra.http.success_response import SuccessResponse


class FastAPIResponse:
    @staticmethod
    def as_json(response: SuccessResponse | ErrorResponse) -> JSONResponse:
        return JSONResponse(
            content=response.model_dump(),
            status_code=response.status,
        )
