from sqlalchemy import Column, Integer, Numeric, ForeignKey
from models import Base
from sqlalchemy.orm import Relationship

class OrderItem(Base):
    __tablename__ = 'order_items'
        
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric, nullable=False)
    
    order = Relationship("Order", back_populates="order_items")
    product = Relationship("Product", back_populates="order_items")