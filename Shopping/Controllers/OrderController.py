from Models import Customer, Order, OrderItem, ShoppingCart, PaymentInfo, Address
from Helpers import getSession

def getAllOrders(user: Customer):
    session = getSession()
    return session.query(Order).filter_by(user_id=user.id).all()

def newOrderFromCart(cart: ShoppingCart, shippingAddress: Address, payment: PaymentInfo) -> Order:
    session = getSession()
    orderInstance = Order(total=cart.total, user_id=cart.user_id, address_id=shippingAddress.address_id, payment_id=payment.payment_id)

    session.add(orderInstance)
    session.commit()
    session.refresh(orderInstance)

    for item in session.query(ShoppingCart).filter_by(cart_id=cart.cart_id).first().items:
        orderItem = OrderItem(subtotal=item.subtotal, quantity=item.quantity, item_id=item.item_id, order_id=orderInstance.order_id)
        session.add(orderItem)
        session.commit()
    
    return orderInstance
