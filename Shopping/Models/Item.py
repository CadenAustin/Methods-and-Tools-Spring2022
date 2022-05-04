from sqlalchemy import Column, Integer, String, Float, ForeignKey

from .Base import Base

class InventoryItem(Base):
    __tablename__ = "InventoryItem"
    item_id = Column(Integer, primary_key=True)
    inv_quantity = Column(Integer)
    title = Column(String)
    description = Column(String)
    genre = Column(String)
    price = Column(Float)
    item_type = Column(String)

    book_reference = Column(Integer, ForeignKey("Book.id"))
    movie_reference = Column(Integer, ForeignKey("Movie.id"))
    
    