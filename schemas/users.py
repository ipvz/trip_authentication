import re

from pydantic import BaseModel, validator
from typing import Optional
from api.dependencies.JWT_config import auth


class SingUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    password2: str
    refresh_token: Optional[str]
    is_staff: Optional[bool]
    is_active: Optional[bool]

    @validator('password')
    def passwords_match(cls, values):
        regex = auth.regex
        if re.fullmatch(regex, values):
            return values
        raise ValueError('The password must be: '
                         'less than six characters, '
                         'contains a lowercase letter, '
                         'contains a capital letter, '
                         'contains a number')


    @validator('password2')
    def comparing_passwords(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('passwords do not match')
        return v

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
