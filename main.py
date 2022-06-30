from fastapi import FastAPI
from endpoints.auth_routes import auth_router
from fastapi_jwt_auth import AuthJWT
from schemes.schemas import Settings


app = FastAPI()


@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(auth_router, tags=['Authentication Path'])