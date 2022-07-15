from typing import List
from sqlalchemy.orm import Session
from models.users import User
from schemas.users import SingUpModel, LoginModel
from fastapi.exceptions import HTTPException
from fastapi import status
from core.hashing_password import get_password, verify_password
import logging
logger = logging.getLogger()

logger.disabled = True


# DAL (Data Access Layer)
class UserOperation:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create_user(self, user: SingUpModel):
        db_email = self.db_session.query(User).filter(User.email == user.email).first()
        if db_email is not None:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with the email already exitst")
        db_username = self.db_session.query(User).filter(User.username == user.username).first()
        if db_username is not None:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with the username already exitst")

        new_user = User(
            username=user.username,
            email=user.email,
            password=get_password(user.password),
            is_active=True,
            is_staff=user.is_staff
        )
        self.db_session.add(new_user)
        self.db_session.commit()
        return HTTPException(status_code=status.HTTP_200_OK, detail="Successful registration")

    async def get_user_by_username(self, user: LoginModel) -> List[User]:
        db_user = self.db_session.query(User).filter(User.username == user.username).first()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Wrong username or password'
            )
        check_password = verify_password(user.password, db_user.password)
        if not check_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Wrong username or password'
            )
        if db_user and check_password:
            return db_user

    async def write_refresh_token(self, user, token):
        user.refresh_token = token
        self.db_session.commit()
        return user

    async def get_user_by_username_str(self, user: str) -> User:
        db_user = self.db_session.query(User).filter(User.username == user).first()
        if db_user:
            return db_user
