from datetime import datetime
from typing import Annotated

from sqlalchemy import func, text
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column


from app.config import get_database_url

DATABASE_URL = get_database_url()

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

int_pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime, mapped_column(server_default=func.now())]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_null_true = Annotated[str, mapped_column(nullable=True)]

async def increment_likes_proc(id_fic: int):
    async with async_session_maker() as session:
        try:
            await session.execute(
                text("CALL increment_likes_proc(:id_fic);"),
                {"id_fic": id_fic}
            )
            await session.commit()
        except Exception as e:
            print(f"An error occurred: {e}")

async def decrement_likes_proc(id_fic: int):
    async with async_session_maker() as session:
        try:
            await session.execute(
                text("CALL decrement_likes_proc(:id_fic);"),
                {"id_fic": id_fic}
            )
            await session.commit()
        except Exception as e:
            print(f"An error occurred: {e}")


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f"{cls.__name__.lower()}s"