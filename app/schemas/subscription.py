from pydantic_settings import BaseSettings


class SubscriptionCreate(BaseSettings):
    name: str
    service: str


class SubscriptionOut(BaseSettings):
    id: int
    name: str
    service: str

    class Config:
        from_attributes = True
