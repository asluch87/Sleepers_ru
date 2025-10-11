import sqlalchemy
from sqlalchemy import engine,MetaData,create_engine,Column,Integer,String,Text,DateTime,ForeignKey
from sqlalchemy.orm import sessionmaker
import psycopg2



def get_db_connection():
  DATABASE_URL = 'postgresql+psycopg2://postgres:admin@192.168.1.132:5432/PROD_Suppliers'
  engine = create_engine(DATABASE_URL) #Создание объекта engine он подключается к БД
  Session = sessionmaker(bind=engine)
  session = Session()
  return session














