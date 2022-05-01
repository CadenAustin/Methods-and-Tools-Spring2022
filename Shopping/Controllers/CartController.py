from Models import Customer, CartItem, InventoryItem, ShoppingCart

def getUserCart(user: Customer) -> ShoppingCart:
    raise NotImplemented

def getItemsInCart(cart: ShoppingCart) -> list[CartItem]:
    raise NotImplemented

def updateCartItem(cart: ShoppingCart, item: InventoryItem, quantity: int) -> bool:
    raise NotImplemented



