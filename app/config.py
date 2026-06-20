from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = Field(validation_alias="DATABASE_URL")


settings = Settings()
