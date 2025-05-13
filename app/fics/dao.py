from sqlalchemy import select, desc

from app.fandoms.models import Fandoms
from app.fics.models import Fics
from app.db import async_session_maker, increment_likes_proc, decrement_likes_proc


class FicDAO:
    @classmethod
    async def find_all_fics(self):
        async with async_session_maker() as session:
            query = select(Fics)
            fics = await session.execute(query)
            return fics.scalars().all()

    @classmethod
    async def find_by_id(self, id_fandom):
        async with async_session_maker() as session:
            query = select(Fics).filter(Fics.id_fandom == id_fandom)
            fics = await session.execute(query)
            return fics.scalars().all()

    @classmethod
    async def find_by_title(self, title):
        async with async_session_maker() as session:
            query = select(Fics).filter(Fics.title == title)
            fic = await session.execute(query)
            return fic.scalars().first()

    @classmethod
    async def create_fic(self, fic):
        async with async_session_maker() as session:
            session.add(fic)
            await session.commit()
            return fic

    @classmethod
    async def update_fic(cls, id_user, id_fic, title = None, description = None, text = None, id_fandom = None):
        async with async_session_maker() as session:
            result = await session.execute(select(Fics).where(Fics.id_fic == id_fic))
            existing_fic = result.scalar_one_or_none()
            if existing_fic:
                if id_user != existing_fic.id_user:
                    raise Exception("Вы не можете редактировать чужой фанфик")
                if title:
                    existing_fic.title = title
                if description:
                    existing_fic.description = description
                if text:
                    existing_fic.text = text
                if id_fandom:
                    existing_fic.id_fandom = id_fandom
                await session.commit()
                return existing_fic
            else:
                raise Exception("Пользователь не найден")

    @classmethod
    async def delete_fic(cls, id_fic, id_user):
        async with async_session_maker() as session:
            result = await session.execute(select(Fics).where(Fics.id_fic == id_fic))
            existing_fic = result.scalar_one_or_none()
            if existing_fic:
                if id_user != existing_fic.id_user:
                    raise Exception("Вы не можете редактировать чужой фанфик")
                await session.delete(existing_fic)
                await session.commit()
            else:
                raise Exception("Фанфик не найден")

    @classmethod
    async def find_by_user(
            cls,
            id_user: int,
            offset: int = 0,
            limit: int = 10
    ):
        async with async_session_maker() as session:
            query = (
                select(Fics)
                .filter(Fics.id_user == id_user)
                .order_by(Fics.published.desc())
                .offset(offset)
                .limit(limit)
            )
            fics = await session.execute(query)
            return fics.scalars().all()

    @classmethod
    async def find_by_fandom(cls, id_fandom):
        async with async_session_maker() as session:
            query = select(Fics).filter(Fics.id_fandom == id_fandom)
            fics = await session.execute(query)
            return fics.scalars().all()

    @classmethod
    async def add_like(cls, id_fic, id_user):
        async with async_session_maker() as session:
            query = select(Fics).filter(Fics.id_fic == id_fic)
            fic = await session.execute(query)
            existing_fic = fic.scalars().first()
        if existing_fic:
            if existing_fic.id_user != id_user:
                await increment_likes_proc(id_fic)
        return

    @classmethod
    async def delete_like(cls, id_fic, id_user):
        async with async_session_maker() as session:
            query = select(Fics).filter(Fics.id_fic == id_fic)
            fic = await session.execute(query)
            existing_fic = fic.scalars().first()
        if existing_fic:
            if existing_fic.id_user != id_user:
                await decrement_likes_proc(id_fic)
        return

    @classmethod
    async def get_top_fics(cls, limit: int = 3):
        async with async_session_maker() as session:
            query = select(Fics).order_by(desc(Fics.likes)).limit(limit)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_all_filtered_fics(cls, filter_query=None):
        async with async_session_maker() as session:
            query = select(Fics)
            if filter_query is not None:
                query = filter_query(query)
            result = await session.execute(query)
            return result.scalars().all()

