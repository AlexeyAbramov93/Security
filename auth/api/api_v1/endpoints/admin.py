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


# Update admin password
@router.put(
    "/",
    response_model=User_Pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def update_admin_password(user: UserIn_Pydantic, admin_user: User_Pydantic = Depends(get_admin_admin)):
    await User.filter(username='admin').update(password_hash=bcrypt.hash(user.password_hash))
    return await User_Pydantic.from_queryset_single(User.get(username='admin'))
