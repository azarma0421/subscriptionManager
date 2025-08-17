from pydantic_settings import BaseSettings


class Token(BaseSettings):
    access_token: str
    token_type: str = "bearer"
