from Controllers import login
from .Menu import menuView
import Helpers.state as state

def loginView():
    if state.user_state: 
        menuView()
    else:
        print("Login:")
        username = input("\tUsername: ")
        password = input("\tPassword: ")
        
        customer = login(username, password)
        if customer:
            state.user_state = customer
            menuView()
        else:
            print("Unsuccessful Login Returning to Welcome Menu\n")
        return