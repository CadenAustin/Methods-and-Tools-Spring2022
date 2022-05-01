from Controllers import register
from .Menu import menuView
import Helpers.state as state

def registerView():
    print("Register:")
    name = input("\tName (optional): ")
    username = input("\tUsername: ")
    password = input("\tPassword: ")
    customer = register(name, username, password)
    if customer:
        state.user_state = customer
        menuView()
    else:
        print("Error creating new customer.\n")
        
