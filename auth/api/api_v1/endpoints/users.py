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


class Status(BaseModel):
    message: str


router = APIRouter()


# Create new user in DB
@router.post(
    "/new_user",
    response_model=User_Pydantic
 )
async def create_user(user: UserIn_Pydantic, admin_user: User_Pydantic = Depends(get_admin_password)):
    user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password_hash), disabled=user.disabled)
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)


# Get user from DB by id
@router.get(
    "/{user_id}",
    response_model=User_Pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def get_user(user_id: int, admin_user: User_Pydantic = Depends(get_admin_password)):
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))


# Get all users from DB
@router.get(
    "/",
    response_model=List[User_Pydantic]
    )
async def get_all_users(admin_user: User_Pydantic = Depends(get_admin_password)):
    return await User_Pydantic.from_queryset(User.all())


# Update user in DB by id
@router.put(
    "/{user_id}",
    response_model=User_Pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def update_user(user_id: int, user: UserIn_Pydantic, admin_user: User_Pydantic = Depends(get_admin_password)):
    #await User.filter(id=user_id).update(**user.dict(exclude_unset=True))
    await User.filter(id=user_id).update(username=user.username, password_hash=bcrypt.hash(user.password_hash), disabled=user.disabled)
    return await User_Pydantic.from_queryset_single(User.get(id=user_id))


# Delete user from DB by id
@router.delete(
    "/{user_id}",
    response_model=Status,
    responses={404: {"model": HTTPNotFoundError}}
)
async def delete_user(user_id: int, admin_user: User_Pydantic = Depends(get_admin_password)):
    deleted_count = await User.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"User {user_id} not found")
    return Status(message=f"Deleted user {user_id}")


# Reset database (Except admin: id and username. Password is set up "admin")
@router.delete(
    "/",
    response_model=Status,
)
async def reset_db(admin_user: User_Pydantic = Depends(get_admin_password)):
    deleted_count = await User.exclude(username='admin').delete()
    await User.filter(username='admin').update(password_hash=bcrypt.hash('admin'))
    return Status(message=f"Database has been reset. Login:admin, Password:admin")