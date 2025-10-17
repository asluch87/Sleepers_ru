from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey,DATETIME
from sqlalchemy.sql import func
from models import Base
from sqlalchemy.orm import Relationship

class Category(Base):
    __tablename__ = 'categories' 
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    slug = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    parent_category_id = Column(Integer, ForeignKey('categories.id'))
    is_active = Column(Boolean, default=True)
    sort_order = Column(Integer, default=0)
    created_at = Column(DATETIME(timezone=False), server_default=func.now())
    
    # Для подкатегорий
    parent = Relationship("Category", remote_side=[id])
    products = Relationship("Product", secondary="product_category", back_populates="categories")