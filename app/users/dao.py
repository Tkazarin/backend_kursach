from sqlalchemy import select
from app.users.models import Users
from app.db import async_session_maker


class UserDAO:
    @classmethod
    async def find_all_users(self):
        async with async_session_maker() as session:
            query = select(Users)
            users = await session.execute(query)
            return users.scalars().all()

    @classmethod
    async def find_by_id(self, id_user):
        async with async_session_maker() as session:
            query = select(Users).filter(Users.id_user == id_user)
            users = await session.execute(query)
            return users.scalars().first()

    @classmethod
    async def find_by_nickname(self, nickname):
        async with async_session_maker() as session:
            query = select(Users).filter(Users.nickname == nickname)
            user = await session.execute(query)
            return user.scalars().first()

    @classmethod
    async def create_user(self, user):
        async with async_session_maker() as session:
            session.add(user)
            await session.commit()

    @classmethod
    async def update_user(cls, user):
        async with async_session_maker() as session:
            result = await session.execute(select(Users).where(Users.id_user == user.id_user))
            existing_user = result.scalar_one_or_none()

            if existing_user:
                existing_user.nickname = user.nickname
                existing_user.password = user.password

                await session.commit()
                return existing_user
            else:
                raise Exception("User not found")
