from fastapi import Depends, FastAPI, HTTPException, Security, status
from tortoise.contrib.fastapi import register_tortoise
from auth.api.api_v1.api import api_router


app = FastAPI()
app.include_router(api_router)


register_tortoise(
    app,
    db_url='sqlite://sql_app.db',
    modules={"models": ["auth.models"]},
    #generate_schemas=True,
    add_exception_handlers=True,
)

# if __name__ == '__main__':
#     uvicorn.run('main:app', port=8000, host='127.0.0.1', reload=True)

