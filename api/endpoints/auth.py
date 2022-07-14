from fastapi import APIRouter, Response, Depends
from schemas.users import SingUpModel, LoginModel
from api.repositories.authentication import authenticate_user
from api.repositories.verification import check_token, check_access_token
from typing import Optional
from fastapi import status, Cookie
from api.session import user_crud
from fastapi.security import OAuth2PasswordBearer

auth_router = APIRouter(
    prefix='/auth'
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@auth_router.post('/singup', status_code=status.HTTP_201_CREATED)
async def sing_up(user: SingUpModel):
    return await user_crud.create_user(user)


@auth_router.post('/login')
async def login(user: LoginModel,  response: Response):
    return await authenticate_user(user_crud, user, response)


# @auth_router.get('/check')
# async def check(response: Response=None, access_token: Optional[str]=Cookie(None), refresh_token: Optional[str]=Cookie(None)):
#     return await check_token(response, access_token, refresh_token)


@auth_router.get('/check')
async def check(token: str = Depends(oauth2_scheme)):
    return await check_access_token(access_token=token)
