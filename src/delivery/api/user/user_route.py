from fastapi import APIRouter
from fastapi.responses import JSONResponse

from src.delivery.api.user.user_register_request import RegisterUserRequest

router = APIRouter(prefix="/users", tags=["Users"])


@router.put("/{id_}")
async def register_user(id_: str, request: RegisterUserRequest) -> JSONResponse:
	raise NotImplementedError