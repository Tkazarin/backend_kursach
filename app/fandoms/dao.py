from sqlalchemy import select, func
from app.fandoms.models import Fandoms
from app.db import async_session_maker
from app.fandoms.filters import FandomFilter


class FandomDAO:
    @classmethod
    async def find_all_fandoms(self):
        async with async_session_maker() as session:
            query = select(Fandoms)
            fandoms = await session.execute(query)
            return fandoms.scalars().all()

    @classmethod
    async def find_by_id(self, id_fandom):
        async with async_session_maker() as session:
            query = select(Fandoms).filter(Fandoms.id_fandom == id_fandom)
            fandoms = await session.execute(query)
            return fandoms.scalars().first()

    @classmethod
    async def find_by_title(self, title):
        async with async_session_maker() as session:
            query = select(Fandoms).filter(Fandoms.title == title)
            fandom = await session.execute(query)
            return fandom.scalars().first()

    @classmethod
    async def create_fandom(self, fandom):
        async with async_session_maker() as session:
            session.add(fandom)
            await session.commit()
            return fandom

    @classmethod
    async def update_fandom(cls, fandom):
        async with async_session_maker() as session:
            result = await session.execute(select(Fandoms).where(Fandoms.id_fandom == fandom.id_fandom))
            existing_fandom = result.scalar_one_or_none()
            if existing_fandom:
                existing_fandom.nickname = fandom.title
                existing_fandom.description = fandom.description
                existing_fandom.type = fandom.type
                await session.commit()
                return existing_fandom
            else:
                raise Exception("Пользователь не найден")

    @classmethod
    async def delete_fandom(cls, id_fandom):
        async with async_session_maker() as session:
            result = await session.execute(select(Fandoms).where(Fandoms.id_fandom == id_fandom))
            existing_fandom = result.scalar_one_or_none()
            if existing_fandom:
                await session.delete(existing_fandom)
                await session.commit()
            else:
                raise Exception("Фанфик не найден")

    @classmethod
    async def get_random_fandoms(cls, limit: int = 3):
        async with async_session_maker() as session:
            query = select(Fandoms).order_by(func.random()).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_filtered_fandoms(cls, fandom_filter: FandomFilter):
        async with async_session_maker() as session:
            statement = select(Fandoms)
            statement = fandom_filter.filter(statement)
            result = await session.execute(statement)
            return result.scalars().all()


