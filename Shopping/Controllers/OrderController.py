from Models import Customer, Order, OrderItem, ShoppingCart, PaymentInfo, Address, InventoryItem, Book, Movie
from Helpers import getSession, flattenEntries

def getAllOrders(user: Customer):
    session = getSession()
    return session.query(Order, Address).filter_by(user_id=user.id).outerjoin(Address, Order.address_id == Address.address_id).all()

def getAllItemsOnOrder(order: Order):
    session = getSession()
    ret = {"books": [], "movies": []}
    ret["books"] = session.query(OrderItem, InventoryItem, Book).filter_by(order_id=order.order_id).join(InventoryItem, OrderItem.item_id == InventoryItem.item_id).join(Book, InventoryItem.book_reference == Book.id).all()
    ret["movies"] = session.query(OrderItem, InventoryItem, Movie).filter_by(order_id=order.order_id).join(InventoryItem, OrderItem.item_id == InventoryItem.item_id).join(Movie, InventoryItem.movie_reference == Movie.id).all()
    return ret

def newOrderFromCart(cart: ShoppingCart, shippingAddress: Address, payment: PaymentInfo) -> Order:
    session = getSession()
    orderInstance = Order(total=cart.total, user_id=cart.user_id, address_id=shippingAddress.address_id, payment_id=payment.payment_id)

    session.add(orderInstance)
    session.commit()

    session.refresh(orderInstance)

    for item in session.query(ShoppingCart).filter_by(cart_id=cart.cart_id).first().items:
        orderItem = OrderItem(subtotal=item.subtotal, item_quantity=item.item_quantity, item_id=item.item_id, order_id=orderInstance.order_id)
        session.add(orderItem)
        session.commit()
    
    return orderInstance