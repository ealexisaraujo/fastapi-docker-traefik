from enum import Enum
from typing import Optional

import ormar
import sqlalchemy
from pydantic import ConfigDict, EmailStr

from .config import settings


def get_async_database_url(url: str) -> str:
    if url.startswith("postgresql://"):
        return url.replace("postgresql://", "postgresql+asyncpg://", 1)
    if url.startswith("postgresql+psycopg2://"):
        return url.replace("postgresql+psycopg2://", "postgresql+asyncpg://", 1)
    return url


def get_sync_database_url(url: str) -> str:
    if url.startswith("postgresql+asyncpg://"):
        return url.replace("postgresql+asyncpg://", "postgresql+psycopg2://", 1)
    return url


database = ormar.DatabaseConnection(get_async_database_url(settings.db_url))
metadata = sqlalchemy.MetaData()
base_ormar_config = ormar.OrmarConfig(database=database, metadata=metadata)


class HairColor(Enum):
    BLACK = "black"
    BLONDE = "blonde"
    BROWN = "brown"
    RED = "red"
    GREY = "grey"
    WHITE = "white"


class User(ormar.Model):
    ormar_config = base_ormar_config.copy(tablename="users")

    id: int = ormar.Integer(primary_key=True)
    email: EmailStr
    active: bool = ormar.Boolean(default=True, nullable=False)


class Person(ormar.Model):
    ormar_config = base_ormar_config.copy(tablename="person")

    id: int = ormar.Integer(primary_key=True)
    first_name: str = ormar.String(nullable=False, max_length=35)
    last_name: str = ormar.String(nullable=False, min_length=3, max_length=35)
    age: int = ormar.Integer(nullable=False, gt=18, lt=115)
    hair_color: Optional[str] = ormar.String(max_length=128, choices=list(HairColor))
    is_married: Optional[bool] = ormar.Boolean(nullable=True, default=False)
    email: EmailStr

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "age": 25,
                "hair_color": "black",
                "is_married": False,
                "email": "john@example.com",
            },
        }
    )


class Location(ormar.Model):
    ormar_config = base_ormar_config.copy(tablename="location")

    id: int = ormar.Integer(primary_key=True)
    city: str = ormar.String(max_length=128, nullable=False)
    state: str = ormar.String(max_length=128, nullable=False)
    country: str = ormar.String(max_length=128, nullable=False)


engine = sqlalchemy.create_engine(get_sync_database_url(settings.db_url))
metadata.create_all(engine)
