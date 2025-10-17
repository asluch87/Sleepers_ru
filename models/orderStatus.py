from sqlalchemy import Column, Integer, String, Text
from models import Base
from sqlalchemy.orm import Relationship

class OrderStatus(Base):
    __tablename__ = 'order_statuses'
        
    id = Column(Integer, primary_key=True)
    status = Column(String(50), nullable=False, unique=True)
    description = Column(Text)

    orders = Relationship("Order", back_populates="order_status")