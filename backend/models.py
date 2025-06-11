from sqlalchemy import Column, Integer, String, Float
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    weight = Column(Float, nullable=True)
    height = Column(Float, nullable=True)
    goal = Column(String, nullable=True)

    avatar_url = Column(String, nullable=True)
