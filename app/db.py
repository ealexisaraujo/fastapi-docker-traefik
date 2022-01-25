from enum import Enum
from typing import Optional

import databases
import ormar
import sqlalchemy
from pydantic import EmailStr

from .config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class HairColor(Enum):
    BLACK = "black"
    BLONDE = "blonde"
    BROWN = "brown"
    RED = "red"
    GREY = "grey"
    WHITE = "white"


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    email: EmailStr
    active: bool = ormar.Boolean(default=True, nullable=False)


class Person(ormar.Model):
    class Meta(BaseMeta):
        tablename = "person"

    id: int = ormar.Integer(primary_key=True)
    first_name: str = ormar.String(nullable=False, max_length=35)
    last_name: str = ormar.String(nullable=False, min_length=3, max_length=35)
    age: int = ormar.Integer(nullable=False, gt=18, lt=115)
    hair_color: Optional[str] = ormar.String(max_length=128, choices=list(HairColor))
    is_married: Optional[bool] = ormar.Boolean(nullable=True, default=False)
    email: EmailStr


class Location(ormar.Model):
    class Meta(BaseMeta):
        tablename = "location"

    id: int = ormar.Integer(primary_key=True)
    city: str = ormar.String(max_length=128, nullable=False)
    state: str = ormar.String(max_length=128, nullable=False)
    country: str = ormar.String(max_length=128, nullable=False)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)
