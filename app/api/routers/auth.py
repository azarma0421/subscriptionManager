from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserOut
from app.schemas.token import Token
from app.services.auth_service import AuthService
from app.api.deps import get_auth_service

authRouter = APIRouter()


@authRouter.post("/register", response_model=UserOut)
def register(user_in: UserCreate, auth: AuthService = Depends(get_auth_service)):
    return auth.register(user_in)


@authRouter.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth: AuthService = Depends(get_auth_service),
):
    user = auth.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    return {"access_token": auth.issue_token_for(user), "token_type": "bearer"}
