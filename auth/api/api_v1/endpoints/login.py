import jwt
import uvicorn

from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from passlib.hash import bcrypt
from auth.models import User, User_Pydantic, UserIn_Pydantic, Token, TokenData

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

from typing import List

from auth.config import SECRET_KEY, ALGORITHM

from auth.dependencies import authenticate_user, create_access_token, get_current_active_user, get_admin_admin, get_admin_password

from fastapi import APIRouter

from pydantic import BaseModel


router = APIRouter()


@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password, form_data.scopes)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )  

    user_obj = await User_Pydantic.from_tortoise_orm(user)

    token = create_access_token(
        data={
            "id": user_obj.id,
            "username": user_obj.username,
            "password_hash": user_obj.password_hash,
            "disabled" : user_obj.disabled,
            "scopes": form_data.scopes
        })
    return {"access_token": token, "token_type": "bearer"}