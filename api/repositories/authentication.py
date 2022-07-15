from fastapi import (
    Response,
    HTTPException,
    status
)
from datetime import timedelta
from typing import Optional
from schemas.users import LoginModel
from api.dependencies.JWT_config import create_jwt_token
from crud.users import UserOperation


async def authenticate_user(user_crud: UserOperation, user: LoginModel, response: Optional[Response] = None):
    user_db = await user_crud.get_user_by_username(user)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Wrong username or password'
        )

    access_payload = {'username': user_db.username, 'aud': 'access'}
    refresh_payload = {'username': user_db.username, 'aud': 'refresh'}

    access_token = create_jwt_token(access_payload)
    refresh_token = create_jwt_token(refresh_payload, timedelta(days=30))

    await user_crud.write_refresh_token(user_db, refresh_token)

    return {'access_token': access_token, 'refresh_token': refresh_token}

