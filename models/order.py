from sqlalchemy import Column, Integer, Numeric, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from models import Base
from sqlalchemy.orm import Relationship

class Order(Base):
    __tablename__ = 'orders' 
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    order_status_id = Column(Integer, ForeignKey('order_statuses.id'), nullable=False)
    total_amount = Column(Numeric, nullable=False)
    shipping_address = Column(Text, nullable=False)
    billing_address = Column(Text, nullable=False)
    customer_notes = Column(Text)
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    updated_at = Column(DateTime(timezone=False), server_default=func.now(), onupdate=func.now())
    
    user = Relationship("User", back_populates="orders")
    order_status = Relationship("OrderStatus", back_populates="orders")
    order_items = Relationship("OrderItem", back_populates="order")
    payments = Relationship("Payment", back_populates="order")