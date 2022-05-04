from .CartController import deleteUserCart

from Models import Address, Customer, PaymentInfo, ShoppingCart
from Helpers import getSession, hashPassword

def checkPassword(customer: Customer, password: str) -> bool:
    return customer and customer.password_hash == hashPassword(password)


def updatePassword(user: Customer, oldPassword: str, newPassword: str) -> bool:
    session = getSession()
    userQuery = session.query(Customer).filter_by(id=user.id)
    if(checkPassword(userQuery.first(), oldPassword)):
        userQuery.update({"password_hash": hashPassword(newPassword)})
        session.commit()
        return True
    
    return False

def updateName(user: Customer, name: str) -> bool:
    session = getSession()
    userQuery = session.query(Customer).filter_by(id=user.id)
    if(userQuery.first()):
        userQuery.update({"name": name})
        session.commit()
        return True
    
    return False


def login(username: str, password: str) -> Customer:
    session = getSession()
    userResult = session.query(Customer).filter_by(username=username).first()
    if userResult and checkPassword(userResult, password):
        return userResult
    return None

def register(name: str, username: str, password: str) -> Customer:
    session = getSession()
    userResult = session.query(Customer).filter_by(username=username).first()
    if not userResult:
        customerInstance = Customer(name=name, username=username, password_hash=hashPassword(password))
        session.add(customerInstance)
        session.commit()

        customer = session.query(Customer).filter_by(username=username).first()
        session.add(ShoppingCart(user_id=customer.id, total=0))
        session.commit()
        
        return session.query(Customer).filter_by(username=username).first()
        

    return None

def attatchPaymentInfoToUser(user: Customer, payment: PaymentInfo) -> None:
    session = getSession()
    session.query(Customer).filter_by(id=user.id).update({"payment_information_id": payment.payment_id})
    session.commit()

def getShippingAddress(user: Customer) -> Address:
    session = getSession()
    return session.query(Address).filter_by(address_id=user.shipping_address_id).first()

def updateShippingAddress(user: Customer, newAddress: Address):
    session = getSession()
    oldAddress = session.query(Address).filter_by(address_id=user.shipping_address_id)
    if (oldAddress.first()):
        oldAddress.delete()
    session.query(Customer).filter_by(id=user.id).update({"shipping_address_id": newAddress.address_id})
    session.commit()

def deleteUser(user: Customer) -> bool:
    session = getSession()
    if (deleteUserCart(user)):
        userFromQuery = session.query(Customer).filter_by(id=user.id).first()
        session.delete(userFromQuery)
        session.commit()

        return True
    return False

