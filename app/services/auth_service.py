from typing import Optional
from fastapi import HTTPException
from app.core.security import get_password_hash, verify_password, create_access_token
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.db.models.user import User

class AuthService:
    def __init__(self, users: UserRepository) -> None:
        self.users = users

    def register(self, user_in: UserCreate) -> User:
        if self.users.get_by_email(user_in.email):
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed = get_password_hash(user_in.password)
        return self.users.create(email=user_in.email, hashed_password=hashed)

    def authenticate(self, email: str, password: str) -> Optional[User]:
        user = self.users.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    def issue_token_for(self, user: User) -> str:
        return create_access_token(subject=user.email)