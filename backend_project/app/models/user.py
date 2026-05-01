from pydantic import BaseModel


class User(BaseModel):
    email: str
    name: str
    role: str
    hashed_password: str

    class Config:
        extra = "forbid"