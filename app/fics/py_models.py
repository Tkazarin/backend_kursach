from datetime import datetime

from pydantic import BaseModel, Field
from typing import Optional

class FicSchema(BaseModel):
    title: str = Field(default=..., min_length=1, max_length=50, description="Название фанфика, от 1 до 50 символов")
    description: str = Field(..., min_length=4, max_length=255, description="Описание, от 4 до 255 символов")
    text: str = Field(..., min_length=2, description="Текст произведения")
    likes: int = Field(default=0, description="Количество лайков")
    title_fandom: str = Field(..., description="Название фандома")

    class Config:
        orm_mode = True
        from_attributes = True

class ShowFicSchema(BaseModel):
    id_fic: Optional[int] = Field(default=None, description="ID фанфика")
    title: str = Field(default=..., min_length=1, max_length=50, description="Название фанфика, от 1 до 50 символов")
    description: str = Field(..., min_length=4, max_length=255, description="Описание, от 4 до 255 символов")
    text: str = Field(..., min_length=2, description="Текст произведения")
    likes: int = Field(default=0, description="Количество лайков")
    published: datetime = Field(..., description="Дата публикации")
    class Config:
        orm_mode = True
        from_attributes = True

class UpdateFicSchema(BaseModel):
    id_fic: int = Field(default=None, description="ID фанфика")
    title: str = Field(default=..., min_length=1, max_length=50, description="Название фанфика, от 1 до 50 символов")
    description: str = Field(..., min_length=4, max_length=255, description="Описание, от 4 до 255 символов")
    text: str = Field(..., min_length=1, description="Текст произведения")
    title_fandom: str = Field(..., description="Фандом")
    class Config:
        orm_mode = True
        from_attributes = True