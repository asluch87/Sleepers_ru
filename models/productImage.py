from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from models import Base
from sqlalchemy.orm import Relationship

class ProductImage(Base):
    __tablename__ = 'product_images'
    
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    image_url = Column(String(500), nullable=False)
    alt_text = Column(String(255))
    sort_order = Column(Integer, default=0)
    is_main = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    
    product = Relationship("Product", back_populates="images")