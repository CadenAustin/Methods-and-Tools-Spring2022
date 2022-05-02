from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from .Base import Base

class Order(Base):
    __tablename__ = "Order"
    order_id = Column(Integer, primary_key=True)
    subtotal = Column(Float)
    total = Column(Float)
    user_id = Column(Integer, ForeignKey("Customer.id"))
    address_id = Column(Integer, ForeignKey("Address.address_id"))
    payment_id = Column(Integer, ForeignKey("PaymentInfo.payment_id"))
    items = relationship("OrderItem", cascade="all, delete", passive_deletes=True)


class OrderItem(Base):
    __tablename__ = "OrderItem"
    id = Column(Integer, primary_key=True)
    subtotal = Column(Float)
    quantity = Column(Integer)
    order_id = Column(Integer, ForeignKey("Order.order_id"))
    item_id = Column(Integer, ForeignKey("InventoryItem.item_id"))
