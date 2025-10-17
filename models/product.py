from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime,Numeric  
from sqlalchemy.sql import func
from sqlalchemy.orm import Relationship
from models import Base

class Product(Base):
    __tablename__ = 'products'
    
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    slug = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, nullable=False)
    sku = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())
    stock = Column(Integer, nullable=False)
    supplier = Column(String, nullable=False)
    image_url = Column(String, nullable=False)
    
    # Простые relationships
    categories = Relationship("Category", secondary="product_category", back_populates="products")
    images = Relationship("ProductImage", back_populates="product")
    order_items = Relationship("OrderItem", back_populates="product")
    basket_items = Relationship("Basket", back_populates="product")
    anonymous_baskets = Relationship("AnonymousBasket", back_populates="product")