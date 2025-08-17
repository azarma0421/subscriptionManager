from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

# --- 設定 JWT ---
SECRET_KEY = "secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- 資料庫設定 ---
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"  # 先用 SQLite，本機方便測試
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# --- 密碼加密 ---
pwd_context = CryptContext(schemes=["bcrypt"])

# --- FastAPI 實例 ---
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# --- 資料庫模型 ---
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    subscriptions = relationship("Subscription", back_populates="owner")


class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    service = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="subscriptions")


Base.metadata.create_all(bind=engine)


# --- Pydantic 模型 ---
class UserCreate(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int
    email: str

    class Config:
        orm_mode = True


class SubscriptionCreate(BaseModel):
    name: str
    service: str


class SubscriptionOut(BaseModel):
    id: int
    name: str
    service: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


# --- 工具函數 ---
def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def authenticate_user(db: Session, email: str, password: str):
    user = get_user(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(lambda: SessionLocal())
):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, email)
    if not user:
        raise credentials_exception
    return user


# --- API 路由 ---
@app.post("/register", response_model=UserOut)
def register(user: UserCreate):
    db = SessionLocal()
    db_user = get_user(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()
    return new_user


@app.post("/token", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": user.email})
    db.close()
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/subscriptions", response_model=SubscriptionOut)
def create_subscription(
    subscription: SubscriptionCreate, current_user: User = Depends(get_current_user)
):
    db = SessionLocal()
    sub = Subscription(
        name=subscription.name, service=subscription.service, owner=current_user
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    db.close()
    return sub


@app.get("/subscriptions", response_model=List[SubscriptionOut])
def list_subscriptions(current_user: User = Depends(get_current_user)):
    db = SessionLocal()
    subs = db.query(Subscription).filter(Subscription.user_id == current_user.id).all()
    db.close()
    return subs
