import jwt

from fastapi import Depends, FastAPI, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, SecurityScopes
from passlib.hash import bcrypt
from auth.models import User, User_Pydantic, UserIn_Pydantic, Token, TokenData

from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise

from typing import List

from auth.config import SECRET_KEY, ALGORITHM


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={"me": "Read information about the current user.", "items": "Read items."},
)


async def authenticate_user(username:str, password:str, scopes:str):
    user = await User.get(username=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


def create_access_token(data: dict):
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))

        token_scopes = payload.get("scopes", [])
        token_data = TokenData(scopes=token_scopes, username=user.username)
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )   
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )

    return await User_Pydantic.from_tortoise_orm(user)


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_admin_admin(user: User = Depends(get_current_user)):
    # Почему здесь не работает user.verify_password('admin'))
    user_obj = await User.get(username=user.username)
    if user.username == 'admin' and user_obj.verify_password('admin'):
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
        )


async def get_admin_password(user: User = Depends(get_current_user)):
    user_obj = await User.get(username=user.username)
    if user.username == 'admin' and not user_obj.verify_password('admin'):
        return user
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
        )