from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Relationship
from models import Base

class Basket(Base):
    __tablename__ = 'basket'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    added_at = Column(DateTime, server_default=func.now())
    order_num = Column(Integer)
    
    user = Relationship("User", back_populates="basket_items")
    product = Relationship("Product", back_populates="basket_items")