from sqlalchemy import Column, Integer, String, ForeignKey

from .Base import Base 

class Customer(Base):
    __tablename__ = "Customer"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    password_hash = Column(String)

    shipping_address_id = Column(Integer, ForeignKey("Address.address_id"))
    payment_information_id = Column(Integer, ForeignKey("PaymentInfo.payment_id"))
    
        
    