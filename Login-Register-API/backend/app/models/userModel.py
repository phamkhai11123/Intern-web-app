from sqlalchemy import Column, String
from ..database import database

class User(database.Base):
    __tablename__ = "users2"
    username = Column(String, primary_key=True, index=True)
    email = Column(String, index=True)
    hashed_password = Column(String)