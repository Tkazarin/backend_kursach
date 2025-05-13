from pydantic import BaseModel, Field
from typing import Optional, Literal

class FandomSchema(BaseModel):
    id_fandom: Optional[int] = Field(default=None, description="ID фандома")
    title: str = Field(default=..., min_length=1, max_length=50, description="Название фандома, от 1 до 50 символов")
    description: str = Field(..., min_length=4, max_length=255, description="Описание, от 4 до 255 символов")
    type: Literal["movie", "game", "cartoon", "series", "literature", "history", "other"] = Field(default="other", description="Тип фандома")
    class Config:
        orm_mode = True
        from_attributes = True