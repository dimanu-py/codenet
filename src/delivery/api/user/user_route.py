from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from src.contexts.social.user.application.register.register_user_command import (
    RegisterUserCommand,
)
from src.contexts.social.user.application.register.user_registrar import UserRegistrar
from src.contexts.social.user.application.unregister.user_unregistrar import (
    UserUnregistrar,
)
from src.contexts.social.user.infra.persistence.in_memory_user_repository import (
    InMemoryUserRepository,
)
from src.delivery.api.user.user_register_request import RegisterUserRequest

router = APIRouter(prefix="/users", tags=["Users"])


@router.put("/{id_}")
async def register_user(id_: str, request: RegisterUserRequest) -> JSONResponse:
    command = RegisterUserCommand(
        id=id_,
        name=request.name,
        username=request.username,
        email=request.email,
        profile_picture=request.profile_picture,
    )
    repository = InMemoryUserRepository()
    user_registrar = UserRegistrar(repository=repository)

    await user_registrar(command)

    return JSONResponse(status_code=status.HTTP_201_CREATED, content={})


@router.delete("/{id_}")
async def unregister_user(id_: str) -> JSONResponse:
    repository = InMemoryUserRepository()
    user_unregistrar = UserUnregistrar(repository=repository)

    await user_unregistrar(id_)

    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content={})
