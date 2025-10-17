from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Relationship
from models import Base

class AnonymousBasket(Base):
    __tablename__ = 'anonymous_basket' 
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(255), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    added_at = Column(DateTime(timezone=False), server_default=func.now())
    
    product = Relationship("Product", back_populates="anonymous_baskets")
    