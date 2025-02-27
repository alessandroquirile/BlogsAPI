from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.utils.database import Base


class Blog(Base):
    __tablename__ = 'blogs'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    written_by = relationship("User", back_populates="blogs")

    def __repr__(self):
        return (
            f"<Blog(id={self.id}, title='{self.title}', "
            f"description='{self.description}', user_id={self.user_id}, "
            f"written_by={self.written_by.username})>"
        )
