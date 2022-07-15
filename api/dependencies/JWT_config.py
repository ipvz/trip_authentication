import random

from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jose import jwt, JWTError
from typing import Optional
from datetime import timedelta, datetime
from uuid import uuid4
from db.database import cfg
from core.RSA_config import pem, key
from models.token import Token

auth = Token(**cfg.auth)

http_bearer = HTTPBearer(auto_error=False, bearerFormat='JWT')



def create_jwt_token(data: dict, expires_delta: Optional[timedelta] = None):
    payload = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=int(auth.access_exp))

    payload.update({'exp': expire, 'jti': str(uuid4())})

    # encoded_jwt = jwt.encode(payload, pem, 'RS512')

    encoded_jwt = jwt.encode(payload, random.choice(auth.secret_words), 'HS256')

    return encoded_jwt


async def access_token_required(
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
    access_token: Optional[str] = Cookie(None)
):
    if not token and access_token:
        jwt_token = access_token
    elif token:
        jwt_token = token.credentials
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authenticated'
        )

    return jwt_token


async def refresh_token_required(
    token: HTTPAuthorizationCredentials = Depends(http_bearer),
    refresh_token: Optional[str] = Cookie(None)
):
    if not token and refresh_token:
        jwt_token = refresh_token
    elif token:
        jwt_token = token.credentials
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not authenticated'
        )

    return jwt_token


async def jwt_decode(jwt_token: str, audience: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={"WWW-Authenticate": "Bearer"}
    )

    # decoded_payload: dict = jwt.decode(jwt_token, key, ['RS512'], audience=audience)
    decoded_payload = None

    for i in auth.secret_words:
        try:
            decoded_payload = jwt.decode(jwt_token, i, ['HS256'], audience=audience)
        except JWTError:
            continue

        public_id: str = decoded_payload.get('username')
        if public_id is None:
            raise credentials_exception

    if decoded_payload is None:
        raise credentials_exception

    return decoded_payload