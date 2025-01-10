from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.put("/{id_}")
async def register_user(id_: str, request: dict) -> JSONResponse:
	raise NotImplementedError