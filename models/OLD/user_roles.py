from sqlalchemy import String,Integer,TEXT,ForeignKey,DateTime,Float,Column
from sqlalchemy.orm import Relationship
from sqlalchemy.sql import func
from models import Base

class User_roles(Base):
    __table_name__ = 'user_roles'
    # Структура
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    description = Column(TEXT)
    created_at = Column(DateTime(timezone=False), server_default=func.now())

    user_roles_id = Relationship('User')