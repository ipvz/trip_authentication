from pydantic.fields import Field
from pydantic.main import BaseModel
from typing import Optional


class Token(BaseModel):
    refresh_token: Optional[str]
    access_exp: Optional[str] = Field(alias='access_token_expiration')
    refresh_exp: Optional[str] = Field(alias='refresh_token_expiration')
    regex: Optional[str] = Field(alias='regex_for_password')
    secret_words: Optional[list]
