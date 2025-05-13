from sqlalchemy.orm import relationship

from app.db import Base
from sqlalchemy import Column, Integer, String


class Fandoms(Base):
    __tablename__ = "fandom"

    id_fandom = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(String(255))
    type = Column(String(255), nullable=False)
    fics = relationship("Fics", back_populates="fandom")

    def __str__(self):
        return f"{self.title}"


