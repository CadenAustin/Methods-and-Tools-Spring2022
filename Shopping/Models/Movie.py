from sqlalchemy import Column, Integer, String
from .Base import Base

class Movie(Base):
    __tablename__ = "Movie"
    id = Column(Integer, primary_key=True)
    director = Column(String)
    leading_actor = Column(String)
    
        