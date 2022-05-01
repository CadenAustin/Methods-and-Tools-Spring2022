from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship

from .Base import Base

class ShoppingCart(Base):
    __tablename__ = "ShoppingCart"
    cart_id = Column(Integer, primary_key=True)
    subtotal = Column(Float)
    total = Column(Float)
    user_id = Column(Integer, ForeignKey("Customer.id"))
    items = relationship("CartItem", cascade="all, delete", passive_deletes=True)
    
class CartItem(Base):
    __tablename__ = "CartItem"
    id = Column(Integer, primary_key=True)
    subtotal = Column(Float)
    quantity = Column(Integer)
    cart_id = Column(Integer, ForeignKey("ShoppingCart.cart_id"))
    item_id = Column(Integer, ForeignKey("InventoryItem.item_id"))