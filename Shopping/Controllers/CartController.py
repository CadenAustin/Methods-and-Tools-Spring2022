from Models import Customer, CartItem, ShoppingCart
from Helpers import getSession
from Models.Item import InventoryItem

def getUserCart(user: Customer) -> ShoppingCart:
    session = getSession()
    return session.query(ShoppingCart).filter_by(user_id=user.id).first()

def getItemsInCart(cart: ShoppingCart):
    session = getSession()
    return session.query(CartItem).filter_by(cart_id=cart.cart_id).all()

def updateCartItem(cart: ShoppingCart, item: InventoryItem, quantity: int):
    if ("InventoryItem" in dir(item)):
        invItem = item.InventoryItem
    else:
        invItem = item
    session = getSession()
    cartQuery = session.query(ShoppingCart).filter_by(cart_id=cart.cart_id)
    itemQuery = session.query(InventoryItem).filter_by(item_id=invItem.item_id)
    cartItem = session.query(CartItem).filter_by(cart_id=cart.cart_id).filter_by(item_id=invItem.item_id)

    priceDiff = 0
    quantityDiff = 0
    if cartItem.first():
        quantityDiff = (quantity - cartItem.first().quantity)
        priceDiff = quantityDiff * invItem.price 
        if quantity == 0:
            cartItem.delete()
        else:
            cartItem.update({CartItem.quantity: quantity, CartItem.subtotal: cartItem.first().subtotal - priceDiff})
    else:
        if quantity != 0:
            quantityDiff = quantity
            priceDiff = (quantity * invItem.price)
            cItem = CartItem(quantity=quantity, cart_id=cart.cart_id, subtotal=priceDiff, item_id=invItem.item_id)
            session.add(cItem)
    cartQuery.update({"total": cartQuery.first().total + priceDiff})
    itemQuery.update({"quantity": itemQuery.first().quantity - quantityDiff})
    session.commit()

#Only call when user is deleted
def deleteUserCart(user: Customer) -> bool:
    session = getSession()
    cartQuery = session.query(ShoppingCart).filter_by(user_id=user.id)
    for cartItem in session.query(CartItem).filter_by(cart_id=cartQuery.first().cart_id).all():
        itemQuery = session.query(InventoryItem).filter_by(item_id=cartItem.item_id)
        updateCartItem(cartQuery.first(), itemQuery.first(), 0)
    cartQuery.delete()
    session.commit()
    return True
    


def resetUserCart(user: Customer) -> bool:
    session = getSession()
    oldCart = session.query(ShoppingCart).filter_by(user_id=user.id).first()
    if oldCart:
        session.delete(oldCart)
    session.add(ShoppingCart(user_id=user.id, total=0))
    session.commit()
    return True

def getCurrentCartQuantity(cart: ShoppingCart, item: InventoryItem) -> int:
    session = getSession()
    cartItem = session.query(CartItem).filter_by(cart_id=cart.cart_id).filter_by(item_id=item.item_id).first()
    return cartItem.quantity if cartItem else 0
