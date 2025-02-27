from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from src.utils.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    blogs = relationship("Blog", back_populates="written_by")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email}), is_admin={self.is_admin}>"
