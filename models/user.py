from sqlalchemy import String,Integer,Text,DateTime,Boolean,ForeignKey,Column
from sqlalchemy.orm import Relationship 
from sqlalchemy.sql import func
from models import Base

#Описание модели
class User(Base):
    __tablename__ = 'users'

       
    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone_number = Column(String(20))
    role_id = Column(Integer, ForeignKey('user_roles.id'), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())
    
    # Связи
    role = Relationship("UserRole", back_populates="users")
    basket_items = Relationship("Basket", back_populates="user")
    orders = Relationship("Order", back_populates="user")

