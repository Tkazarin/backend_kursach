from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Text, ForeignKey, DateTime

from app.db import Base


class Comments(Base):
    __tablename__ = "comment"

    id_comment = Column(Integer, primary_key=True)
    text = Column(Text, nullable=False)
    published = Column(DateTime)
    id_user = Column(Integer, ForeignKey("user.id_user"), nullable=False)
    id_fic = Column(Integer, ForeignKey("fic.id_fic"), nullable=False)
    user = relationship("Users", back_populates="comments")
    fics = relationship("Fics", back_populates="comments")
