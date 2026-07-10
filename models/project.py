from sqlalchemy import Column, Integer, String, Float, Text, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from database.base import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), nullable=False)
    details = Column(Text, nullable=False)
    total_target = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    owner = relationship("User", back_populates="projects")

    def __repr__(self) -> str:
        return f"<Project id={self.id} title='{self.title}' owner_id={self.owner_id}>"
