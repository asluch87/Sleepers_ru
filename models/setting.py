from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from models import Base

class Setting(Base):
    __tablename__ = 'settings'

        
    id = Column(Integer, primary_key=True)
    setting_key = Column(String(255), nullable=False, unique=True)
    setting_value = Column(Text)
    description = Column(Text)
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())