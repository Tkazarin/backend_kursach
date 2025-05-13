from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime

from app.db import Base


class Fics(Base):
    __tablename__ = "fic"

    id_fic = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    text = Column(Text, nullable=False)
    likes = Column(Integer, default=0)
    published = Column(DateTime)
    id_user = Column(Integer, ForeignKey("user.id_user"), nullable=False)
    id_fandom = Column(Integer, ForeignKey("fandom.id_fandom"), nullable=False)
    user = relationship("Users", back_populates="fics")
    fandom = relationship("Fandoms", back_populates="fics")
    comments = relationship("Comments", back_populates="fics")
