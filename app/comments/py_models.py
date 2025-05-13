from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional

class CommentSchema(BaseModel):
    id_fic: int = Field(default=None, description="ID фанфика")
    text: str = Field(..., min_length=2, description="Текст произведения")

    class Config:
        orm_mode = True
        from_attributes = True

class ShowCommentSchema(BaseModel):
    id_comment: Optional[int] = Field(default=None, description="ID комментария")
    id_user: int = Field(default=None, description="ID пользователя")
    text: str = Field(..., min_length=2, description="Текст комментария")
    published: datetime = Field(..., description="Дата публикации")
    class Config:
        orm_mode = True
        from_attributes = True

class UpdateCommentSchema(BaseModel):
    id_comment: int = Field(default=None, description="ID комментария")
    text: str = Field(..., min_length=1, description="Текст комментария")
    class Config:
        orm_mode = True
        from_attributes = True