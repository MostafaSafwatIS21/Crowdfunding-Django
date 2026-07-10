from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from database.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(100), nullable=False)  # holds hashed bcrypt password
    phone = Column(String(20), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email} name={self.first_name} {self.last_name}>"
