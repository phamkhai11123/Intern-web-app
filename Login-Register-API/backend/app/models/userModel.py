from sqlalchemy import Column, String, DateTime,Integer
from sqlalchemy.sql import func
from ..database import database
# from ..database.database import Base
from pydantic import BaseModel


class User(database.Base):
    __tablename__ = "users2"


    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    username = Column(String, index=True)
    email = Column(String, index=True)
    hashed_password = Column(String)  
    role = Column(String) 
    created_at = Column(DateTime(timezone=True), server_default=func.now())

