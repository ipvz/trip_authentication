from typing import Optional
from pydantic import validator, Field, BaseModel
from pydantic_yaml import YamlModel


class Config(YamlModel):
    psql: dict


class Settings(BaseModel):
    PSQL_HOST: str = Field(alias='host')
    PSQL_USER: str = Field(alias='user')
    PSQL_PASSWD: str = Field(alias='passwd')
    PSQL_DB: str = Field(alias='database')
    PSQL_PORT: int = Field(alias='port')

    DATABASE_URI: Optional[dict] = None

    @validator("DATABASE_URI", always=True)
    def assemble_db_connection(cls, value, values) -> str:
        scheme = "postgresql"
        return f'{scheme}://{values["PSQL_USER"]}:{values["PSQL_PASSWD"]}@{values["PSQL_HOST"]}:{values["PSQL_PORT"]}/{values["PSQL_DB"]}'
