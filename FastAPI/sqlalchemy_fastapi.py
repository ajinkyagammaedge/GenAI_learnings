from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from databases import Database
import enum

DATABASE_URL = "sqlite:///./patient.db"

engine= create_engine(DATABASE_URL, connect_args={"check_same_thread":False})
sessionlocal= sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()

database = Database(DATABASE_URL)

class genderenum(enum.Enum):
    male='male'
    female='female'
    others= 'others'

class User(Base):
    __tablename__= "patient"

    id = Column(String, primary_key=True, index=True)
    name= Column(String, nullable=True)
    city= Column(String, nullable=True)
    age= Column(Integer, nullable=True)
    gender= Column(enum(genderenum), nullable=True)
    height= Column(float, nullable=True)
    weight= Column(float, nullable=True)










class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())