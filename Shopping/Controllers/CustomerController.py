import hashlib

from Models import Customer, ShoppingCart
from Helpers import getSession

def checkPassword(customer: Customer, password: str) -> bool:
        return customer.password_hash == hashPassword(password)

def hashPassword(password: str) -> str:
        return hashlib.sha256(password.encode('utf_8')).hexdigest()

def login(username: str, password: str) -> Customer:
    session = getSession()
    userResult = session.query(Customer).filter_by(username=username).first()
    if userResult and checkPassword(userResult, password):
        return userResult
    return None

def register(name: str, username: str, password: str) -> Customer:
    session = getSession()
    userResult = session.query(Customer).filter_by(username=username).first()
    print(userResult)
    if not userResult:
        customerInstance = Customer(name=name, username=username, password_hash=hashPassword(password))
        session.add(customerInstance)
        session.commit()

        customer = session.query(Customer).filter_by(username=username).first()
        session.add(ShoppingCart(user_id=customer.id))
        session.commit()
        
        return session.query(Customer).filter_by(username=username).first()
        

    return None