from fastapi import APIRouter

from auth.api.api_v1.endpoints import admin, login, me, users

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(me.router, prefix="/me", tags=["me"])
