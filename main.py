from fastapi import FastAPI
from api.endpoints.auth import auth_router

app = FastAPI()

app.include_router(auth_router, tags=['Authentication Path'])