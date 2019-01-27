from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

# Write your classes here :
class Account(Base):
    __tablename__ = "accounts"
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, primary_key = True)
    password= Column(String)
    age = Column(String)

class Info(Base):
	"""docstring for add_info"""
	__tablename__="info"
	identity = Column(Integer, primary_key = True, autoincrement=True)
	name = Column(String)
	quantity = Column(Integer)	
	submitted = Column(String)