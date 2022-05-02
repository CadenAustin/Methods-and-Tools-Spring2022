from sqlalchemy import Column, Integer, String
from .Base import Base

class Address(Base):
    __tablename__ = "Address"

    address_id = Column(Integer, primary_key=True)
    street_one = Column(String)
    street_two = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(Integer)
 
    def __repr__(self):  
        return f'{self.street_one}\n{self.street_two}\n{self.city}, {self.state} {self.zip}'
