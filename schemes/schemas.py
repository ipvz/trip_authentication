from pydantic import BaseModel
from typing import Optional


class SingUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
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


class Settings(BaseModel):
    authjwt_secret_key: str = '8cb8002e3530583960b9b4f19a0947eb107d4a7fb9fa4099a7e752598f23f5ad'


class LoginModel(BaseModel):
    username: str
    password: str