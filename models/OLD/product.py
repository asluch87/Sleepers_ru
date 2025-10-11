from sqlalchemy import Column,Integer,String,DateTime,ForeignKey,text,Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import Relationship
from models import Base



class Product (Base):


    id = Column(Integer,primary_key= True)
    name= Column (String,nullable= False)
    slug = Column(String,nullable= False)
    description = Column(text, nullable = False)
    price = Column (Integer,nullable = False )
    stock_quantity = Column (Integer, nullable= False)
    sku = Column (String,nullable=False)

    is_active = Column(Boolean,nullable = False)
    created_at = Column(DateTime(timezone=False),  server_default=func.now())
    updated_at = Column(DateTime(timezone=False), server_default= func.now())

    stock = Column (Integer,nullable = False )
    supplier = Column(String,nullable= False)
    image_url = Column(String,nullable= False)



  
    basket_items = Relationship("Basket")
    




