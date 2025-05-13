from sqlalchemy.orm import relationship

from app.db import Base
from sqlalchemy import Column, Integer, String, Boolean


class Users(Base):
    __tablename__ = "user"

    id_user = Column(Integer, primary_key=True)
    nickname = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    is_superuser = Column(Boolean, default=False)
    fics = relationship("Fics", back_populates="user")
    comments = relationship("Comments", back_populates="user")

    def __str__(self):
        return f"{self.nickname}"


