from fastapi import FastAPI
from app.api.routers.auth import authRouter
from app.api.routers.subscriptions import subRouter

app = FastAPI()

app.include_router(authRouter, prefix="/auth", tags=["auth"])
app.include_router(subRouter, prefix="/subscriptions", tags=["subscriptions"])


@app.get("/")
def read_root():
    return {"status": "ok"}
