from pydantic import BaseModel, Field


class UserSignupRequest(BaseModel):
    name: str = Field(examples=["John Doe"])
    username: str = Field(examples=["johndoe"])
    email: str = Field(examples=["johndoe@hotmail.com"])
