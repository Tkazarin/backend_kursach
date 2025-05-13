from pydantic import BaseModel, Field, EmailStr

class UserSchema(BaseModel):
    student_id: int
    name: str = Field(default=..., min_length=1, max_length=50, description="Имя студента, от 1 до 50 символов")
    email: EmailStr = Field(default=..., description="Электронная почта студента")
    password: str = Field(...)