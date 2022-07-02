from pydantic import BaseModel
from typing import Optional


class SingUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    refresh_token: Optional[str]
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'username': 'vladislav',
                'email': 'vladislav@gmail.com',
                'password': 'password',
                'is_staff': False,
                'is_active': True
            }
        }


class LoginModel(BaseModel):
    username: str
    password: str


class UserOutDb(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'username': 'vladislav',
                'email': 'vladislav@gmail.com',
            }
        }
