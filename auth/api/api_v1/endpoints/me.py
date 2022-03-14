from fastapi import Depends, FastAPI, HTTPException, Security, status
from passlib.hash import bcrypt
from auth.models import User, User_Pydantic, UserIn_Pydantic, Token, TokenData

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

from auth.dependencies import get_current_active_user

from fastapi import APIRouter


router = APIRouter()


# Get authorized user info
@router.get("/", response_model=User_Pydantic)
async def get_user(user: User_Pydantic = Depends(get_current_active_user)):
    return user

# Пользователю, который знает свой пароль особо менять то его не требуется
# Надо делать восстановление пароля через почту 
# Update authorized user password
@router.put(
    "/",
    response_model=User_Pydantic,
    responses={404: {"model": HTTPNotFoundError}}
)
async def update_authorized_user_data(
    user: UserIn_Pydantic,
    current_active_user: User_Pydantic = Depends(get_current_active_user)
):
    await User.filter(username=user.username).update(password_hash=bcrypt.hash(user.password_hash))
    return await User_Pydantic.from_queryset_single(User.get(username=user.username))


# @router.get("/users/me/items/", tags=["users"])
# async def read_own_items(current_user: User = Security(get_current_active_user, scopes=["items"])):
#     return [{"item_id": current_user.id, "owner": current_user.username}]

# @router.get("/status/")
# async def read_system_status(current_user: User = Depends()):
#     return {"disabled": current_user.disabled}