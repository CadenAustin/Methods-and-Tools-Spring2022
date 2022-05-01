from sqlalchemy import Column, Integer, String
from .Base import Base

class Book(Base):
    __tablename__ = "Book"
    id = Column(Integer, primary_key=True)
    author = Column(String)
    publisher = Column(String)
    isbn = Column(String)

        