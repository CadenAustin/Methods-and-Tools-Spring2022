from Models import Address, Customer, PaymentInfo, Order
from Helpers import getSession

def newPaymentInfo(card_number, cvv, expiration) -> PaymentInfo:
    session = getSession()
    paymentInstance = PaymentInfo(card_number=card_number, cvv=cvv, expiration=expiration)

    session.add(paymentInstance)
    session.commit()

    session.refresh(paymentInstance)
    return paymentInstance

def getPaymentInfo(user: Customer) -> PaymentInfo:
    session = getSession()
    return session.query(PaymentInfo).filter_by(payment_id=user.payment_information_id).first()
    
def attatchAddressToPayment(payment: PaymentInfo, address: Address) -> None:
    session = getSession()
    session.query(PaymentInfo).filter_by(payment_id=payment.payment_id).update({"billing_address_id": address.address_id})
    session.commit()

def deletePaymentInfo(payment: PaymentInfo):
    session = getSession()
    if (not session.query(Order).filter_by(payment_id=payment.payment_id).all()):
        session.delete(session.query(PaymentInfo).filter_by(payment_id=payment.payment_id).first())
        session.commit()
