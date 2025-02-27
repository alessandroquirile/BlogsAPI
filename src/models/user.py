from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.utils.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    blogs = relationship("Blog", back_populates="written_by")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"
