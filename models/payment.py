from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.sql import func
from models import Base
from sqlalchemy.orm import Relationship

class Payment(Base):
    __tablename__ = 'payments'
        
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    payment_method = Column(String(50), nullable=False)
    amount = Column(Numeric, nullable=False)
    status = Column(String(50), nullable=False)
    transaction_id = Column(String(255))
    created_at = Column(DateTime(timezone=False), server_default=func.now())
    
    order = Relationship("Order", back_populates="payments")