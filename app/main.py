from fastapi import FastAPI
from app.api.routers.auth import authRouter
from app.api.routers.subscriptions import subscriptionsRouter
from app.api.routers.recommendations import recommendationsRouter

app = FastAPI()

app.include_router(authRouter, prefix="/auth", tags=["auth"])
app.include_router(subscriptionsRouter, prefix="/subscriptions", tags=["subscriptions"])
app.include_router(
    recommendationsRouter, prefix="/recommendations", tags=["recommendations"]
)


@app.get("/")
def read_root():
    return {"status": "ok"}
