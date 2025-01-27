from fastapi import FastAPI

from src.social.user.infra.router import signup_user_router as signup_user


app = FastAPI()

app.include_router(signup_user.router)
