from pydantic.main import BaseModel


class RefreshToken(BaseModel):
    refresh_token: str
