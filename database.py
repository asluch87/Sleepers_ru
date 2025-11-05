import sqlalchemy
from sqlalchemy import engine,MetaData,create_engine,Column,Integer,String,Text,DateTime,ForeignKey
from sqlalchemy.orm import sessionmaker
import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()


# Себе для напоминания на сетевом хранилище ip не статика, поэтому проблема с подключением дата аренды видимо закончилась. ИСполбзовать мигрированную БД с локалхоста



def get_db_connection():
    # Получаем все данные из переменных окружения
    db_user = os.getenv('DB_USER', 'postgres')  
    db_password = os.getenv('DB_PASSWORD')

    db_host = os.getenv('DB_HOST', 'localhost')

    db_host = os.getenv('DB_HOST', 'asluchSetevoeChranSluch')

    db_port = os.getenv('DB_PORT', '5432')
    db_name = os.getenv('DB_NAME', 'PROD_Suppliers')
    
    if not db_password:
        raise ValueError("Проверь пароль")
    
    # Формируем URL подключения в вид е строкки 
    DATABASE_URL = f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

















