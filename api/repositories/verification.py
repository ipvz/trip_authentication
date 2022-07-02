from api.dependencies.JWT_config import jwt_decode, create_jwt_token
from fastapi import Cookie
from typing import Optional
from datetime import timedelta
from api.session import user_crud
from jose import jwt, JWTError
from core.RSA_config import key
from fastapi import (
    Response,
    HTTPException,
    status
)


async def check_token(response: Optional[Response]=None, access_token: Optional[str]=Cookie(None), refresh_token: Optional[str]=Cookie(None)):
    try:
        decoded_payload: dict = jwt.decode(access_token, key, ['RS512'], audience='access')
        print(f"decoded_payload - {decoded_payload}")
        return decoded_payload
    except JWTError:
        decoded_username = (await jwt_decode(refresh_token, 'refresh'))['username']
        user_db = await user_crud.get_user_by_username_str(decoded_username)
        if user_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='User not found'
            )
        if user_db.refresh_token == refresh_token:
            access_payload = {'username': user_db.username, 'aud': 'access'}
            refresh_payload = {'username': user_db.username, 'aud': 'refresh'}

            access_token = create_jwt_token(access_payload)
            refresh_token = create_jwt_token(refresh_payload, timedelta(days=30))

            await user_crud.write_refresh_token(user_db, refresh_token)

            response.set_cookie(key='access_token', value=access_token, httponly=True)
            response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)

            return {'detail': 'Tokens successfully updated'}
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token'
            )