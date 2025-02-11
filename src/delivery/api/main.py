from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.shared.infra.HttpResponse import HttpResponse
from src.social.user.infra.router import signup_user_router as signup_user

app = FastAPI()

app.include_router(signup_user.router)


@app.exception_handler(Exception)
async def unexpected_exception_handler(_: Request, exc: Exception) -> JSONResponse:
    return HttpResponse.internal_error()
