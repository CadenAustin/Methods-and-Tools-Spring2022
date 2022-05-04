from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from .Base import Base 

class Customer(Base):
    __tablename__ = "Customer"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    password_hash = Column(String)

    shippingAddress = relationship("Address", cascade="all,delete", backref="user")
    shipping_address_id = Column(Integer, ForeignKey("Address.address_id"))
    paymentInformation = relationship("PaymentInfo", cascade="all,delete", backref="user")
    payment_information_id = Column(Integer, ForeignKey("PaymentInfo.payment_id"))

    orders = relationship("Order", cascade="all,delete", backref="user")
    
        
    