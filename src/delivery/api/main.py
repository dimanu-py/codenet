from fastapi import FastAPI
from src.delivery.api.user import user_route as users


app = FastAPI()

app.include_router(users.router)
