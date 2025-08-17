from pydantic_settings import BaseSettings


class UserCreate(BaseSettings):
    email: str
    password: str


class UserOut(BaseSettings):
    id: int
    email: str

    class Config:
        from_attributes = True
