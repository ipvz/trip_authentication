import time
from api.dependencies.JWT_config import jwt_decode, create_jwt_token
from typing import Optional
from datetime import timedelta
from api.session import user_crud
from jose import jwt, JWTError
from core.RSA_config import key
from fastapi import (
    HTTPException,
    status
)


async def refresh_token(token: Optional[str]):
    decoded_username = (await jwt_decode(token, 'refresh'))['username']
    user_db = await user_crud.get_user_by_username_str(decoded_username)
    if user_db is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    elif user_db.refresh_token == token:

        access_payload = {'username': user_db.username, 'aud': 'access'}
        refresh_payload = {'username': user_db.username, 'aud': 'refresh'}

        access_token = create_jwt_token(access_payload)
        refresh_token = create_jwt_token(refresh_payload, timedelta(days=30))

        await user_crud.write_refresh_token(user_db, refresh_token)

        return {'access_token': access_token, 'refresh_token': refresh_token}
    else:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token invalid'
        )


async def check_access_token(access_token: Optional[str]):
    try:
        decoded_payload: dict = jwt.decode(access_token, key, ['RS512'], audience='access')
        time_exp = time.strftime('%H:%M:%S %d.%m.%Y', time.localtime(decoded_payload['exp']))
        decoded_payload.update({'exp': time_exp})
        return decoded_payload
    except JWTError:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")
