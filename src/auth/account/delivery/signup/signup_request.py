from pydantic import BaseModel, Field


class SignupRequest(BaseModel):
    username: str = Field(examples=["johndoe"])
    email: str = Field(examples=["johndoe@hotmail.com"])
    password: str = Field(examples=["strongpassword123"])
