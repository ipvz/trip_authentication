from fastapi import FastAPI
from api.endpoints.auth import auth_router
from db.init_bd import init_db

app = FastAPI(openapi_url='/api/auth/openapi.json', docs_url='/auth/docs')

app.include_router(auth_router, tags=['Authentication Path'])


@app.on_event("startup")
async def startup_event():
    init_db()


# docker run --network=host auth