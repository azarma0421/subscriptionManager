from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./test.db"


settings = Settings()
