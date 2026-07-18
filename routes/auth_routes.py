from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime

from models import RegisterRequest, LoginRequest, TokenResponse
from database.collections import users_collection
from auth.password import hash_password, verify_password
from auth.jwt_handler import create_access_token
from auth.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
def register_user(data: RegisterRequest):
    existing_user = users_collection.find_one({"email": data.email})

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    user_doc = {
        "name": data.name,
        "email": data.email,
        "password": hash_password(data.password),
        "created_at": datetime.utcnow()
    }

    result = users_collection.insert_one(user_doc)

    return {
        "message": "User registered successfully",
        "user_id": str(result.inserted_id),
        "email": data.email
    }


@router.post("/login", response_model=TokenResponse)
def login_user(data: LoginRequest):
    user = users_collection.find_one({"email": data.email})

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    if not verify_password(data.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {
            "user_id": str(user["_id"]),
            "email": user["email"]
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/me")
def get_me(current_user=Depends(get_current_user)):
    return {
        "message": "Current logged in user",
        "user": {
            "id": current_user["_id"],
            "name": current_user["name"],
            "email": current_user["email"]
        }
    }