from sqlalchemy import select
from app.comments.models import Comments
from app.db import async_session_maker


class CommentDAO:
    @classmethod
    async def find_all_fics(self):
        async with async_session_maker() as session:
            query = select(Comments)
            comments = await session.execute(query)
            return comments.scalars().all()

    @classmethod
    async def find_by_id(self, id_comment):
        async with async_session_maker() as session:
            query = select(Comments).filter(Comments.id_comment == id_comment)
            comments = await session.execute(query)
            return comments.scalars().first()


    @classmethod
    async def create_comment(self, comment):
        async with async_session_maker() as session:
            session.add(comment)
            await session.commit()
            return comment

    @classmethod
    async def update_comment(cls, id_user, id_comment, text):
        async with async_session_maker() as session:
            result = await session.execute(select(Comments).where(Comments.id_comment == id_comment))
            existing_comment = result.scalar_one_or_none()
            if existing_comment:
                if id_user != existing_comment.id_user:
                    raise Exception("Вы не можете редактировать чужой комментарий")
                if text:
                    existing_comment.text = text
                await session.commit()
                return existing_comment
            else:
                raise Exception("Комментарий не найден")

    @classmethod
    async def delete_comment(cls, id_comment, id_user):
        async with async_session_maker() as session:
            result = await session.execute(select(Comments).where(Comments.id_comment == id_comment))
            existing_comment = result.scalar_one_or_none()
            if existing_comment:
                if id_user != existing_comment.id_user:
                    raise Exception("Вы не можете редактировать чужой комментарий")
                await session.delete(existing_comment)
                await session.commit()
            else:
                raise Exception("Комментарий не найден")

    @classmethod
    async def find_by_fic(cls, id_fic):
        async with async_session_maker() as session:
            query = select(Comments).filter(Comments.id_fic == id_fic)
            comments = await session.execute(query)
            return comments.scalars().all()