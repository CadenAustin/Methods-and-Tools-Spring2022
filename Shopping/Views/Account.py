import sys

from Helpers import getSession
import Helpers.state as state
from Models import Customer
from Controllers import updateShippingAddress, updatePassword, updateName, deleteUser
from .Order import orderView
from .Address import addressView
from .Payment import paymentView

def updateState():
    session = getSession()
    state.user_state = session.query(Customer).filter_by(id=state.user_state.id).first()

#return True if delete Account
def accountView():
    while 1:
        print(f"\nUser: {state.user_state.username if len(state.user_state.name) == 0 else state.user_state.name}")
        print("Please Select From The Following Options:\n[o] - view your previous orders\n[p] - change your password\n[n] - change your name\n[s] - update or add a default shipping address\n[m] - update or add a new payment method\n[d] - delete account\n[r] - return\n[x] - Exit\n")
        option = input("Your Input: ").lower()
        if option == "o":
            orderView()
        elif option ==  "p":
            oldPass = input("What is your old password: ")
            newPass = input("What would you like to set your password to: ")
            print ("Success" if updatePassword(state.user_state, oldPass, newPass) else "Error in updating password")
        elif option == "n":
            name = input("What name would you like to change to: ")
            print ("Success" if updateName(state.user_state, name) else "Error in updating name")
        elif option == "s":
            createdAddress = addressView()
            if createdAddress:
                updateShippingAddress(state.user_state, createdAddress)
        elif option == "m":
            paymentView()
        elif option == "d":
            confirm = input("\tAre you sure you want to delete your account [y]: ").lower()
            if confirm == "y":
                if (deleteUser(state.user_state)):
                    state.user_state = None
                    return True
            print("Aborting Delete")
        elif option == "r":
            return None
        elif option == "x":
            sys.exit(0)
        updateState()