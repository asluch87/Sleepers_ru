from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import Relationship
from sqlalchemy.sql import func
from models import Base

class UserRole(Base):
    __tablename__ = 'user_roles'

    
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(Text)
    created_at = Column(DateTime(timezone=False), server_default=func.now())

    users = Relationship("User", back_populates="role")