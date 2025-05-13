from pydantic import BaseModel, Field

class UserSchema(BaseModel):
    nickname: str = Field(default=..., min_length=1, max_length=50, description="Имя студента, от 1 до 50 символов")
    password: str = Field(..., min_length=4, max_length=20, description="Пароль, от 4 до 20 символов")

class UserResponse(BaseModel):
    nickname: str

    class Config:
        orm_mode = True
        from_attributes = True
