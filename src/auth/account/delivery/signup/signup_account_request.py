from pydantic import BaseModel, Field


class SignupAccountRequest(BaseModel):
    username: str = Field(examples=["johndoe"])
    email: str = Field(examples=["johndoe@hotmail.com"])
    password: str = Field(examples=["strongpassword123"])
