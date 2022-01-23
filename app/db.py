from typing import Optional
import databases
import ormar
import sqlalchemy

from .config import settings

database = databases.Database(settings.db_url)
metadata = sqlalchemy.MetaData()


class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class User(ormar.Model):
    class Meta(BaseMeta):
        tablename = "users"

    id: int = ormar.Integer(primary_key=True)
    email: str = ormar.String(max_length=128, unique=True, nullable=False)
    active: bool = ormar.Boolean(default=True, nullable=False)

class Person(ormar.Model):
    class Meta(BaseMeta):
        tablename = "person"
    id: int = ormar.Integer(primary_key=True)
    first_name: str = ormar.String(max_length=128, nullable=False)
    last_name: str = ormar.String(max_length=128, nullable=False)
    age: int = ormar.Integer(nullable=False)
    hair_color:Optional[str] = ormar.String(max_length=128, nullable=True)
    is_married:Optional[bool] = ormar.Boolean(nullable=True, default=False)


engine = sqlalchemy.create_engine(settings.db_url)
metadata.create_all(engine)