from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import jwt
import bcrypt
from typing import Optional
from jose import JWTError, jwt as jwt_lib

router = APIRouter()

# PyJWT settings
SECRET_KEY = "your-secret-key-here-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# User storage (use database in production)
users_db = {
    "user1": {"email": "user@example.com", "hashed_password": bcrypt.hashpw(b"password", bcrypt.gensalt()).decode()},
}

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt_lib.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/register", response_model=dict)
async def register(request: RegisterRequest):
    if request.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = bcrypt.hashpw(request.password.encode(), bcrypt.gensalt()).decode()
    users_db[request.email] = {"email": request.email, "hashed_password": hashed}
    return {"message": "User registered successfully", "email": request.email}

@router.post("/login", response_model=Token)
async def login(request: LoginRequest):
    user_data = users_db.get(request.email)
    if not user_data or not verify_password(request.password, user_data["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(data={"sub": request.email})
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=dict)
async def get_current_user():
    # In production, extract token from headers and decode
    pass

@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}
