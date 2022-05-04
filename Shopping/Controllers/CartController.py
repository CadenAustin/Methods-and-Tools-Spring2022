from Models import Customer, CartItem, ShoppingCart, Movie, Book
from Helpers import getSession
from Models.Item import InventoryItem

def getUserCart(user: Customer) -> ShoppingCart:
    session = getSession()
    return session.query(ShoppingCart).filter_by(user_id=user.id).first()

def getItemsInCart(cart: ShoppingCart):
    session = getSession()
    ret = {"books": [], "movies": []}
    ret["books"] = session.query(CartItem, InventoryItem, Book).filter_by(cart_id=cart.cart_id).join(InventoryItem, CartItem.item_id == InventoryItem.item_id).join(Book, InventoryItem.book_reference == Book.id).all()
    ret["movies"] = session.query(CartItem, InventoryItem, Movie).filter_by(cart_id=cart.cart_id).join(InventoryItem, CartItem.item_id == InventoryItem.item_id).join(Movie, InventoryItem.movie_reference == Movie.id).all()
    return ret

def updateCartItem(cart: ShoppingCart, item: InventoryItem, quantity: int):
    try:
        invItem = item.InventoryItem
    except:
        invItem = item
    session = getSession()
    cartQuery = session.query(ShoppingCart).filter_by(cart_id=cart.cart_id)
    itemQuery = session.query(InventoryItem).filter_by(item_id=invItem.item_id)
    cartItem = session.query(CartItem).filter_by(cart_id=cart.cart_id).filter_by(item_id=invItem.item_id)

    priceDiff = 0
    quantityDiff = 0
    if cartItem.first():
        quantityDiff = (quantity - cartItem.first().item_quantity)
        priceDiff = quantityDiff * invItem.price 
        if quantity == 0:
            cartItem.delete()
        else:
            cartItem.update({CartItem.item_quantity: quantity, CartItem.subtotal: f"{float(cartItem.first().subtotal) + priceDiff:.2f}"})
    else:
        if quantity != 0:
            quantityDiff = quantity
            priceDiff = (quantity * invItem.price)
            cItem = CartItem(item_quantity=quantity, cart_id=cart.cart_id, subtotal=f"{priceDiff:.2f}", item_id=invItem.item_id)
            session.add(cItem)
    cartQuery.update({"total": f"{cartQuery.first().total + priceDiff:.2f}"})
    itemQuery.update({"inv_quantity": itemQuery.first().inv_quantity - quantityDiff})
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
    return cartItem.item_quantity if cartItem else 0

def getCartItem(cart_item_id) -> InventoryItem:
    session = getSession()
    cart_item =  session.query(CartItem).filter_by(cart_item_id=cart_item_id).first()
    return session.query(InventoryItem).filter_by(item_id=cart_item.item_id).first()