import sys

from Controllers import getItemsInCart, getShippingAddress, getUserCart, newOrderFromCart, updateShippingAddress
from Controllers.CartController import resetUserCart
import Helpers.state as state
from .Payment import paymentView
from .Address import addressView

def cartView():
    while 1:
        cart = getUserCart(state.user_state)
        cartItems = getItemsInCart(cart)
        [print(f"{i}") for i in cartItems]
        print(f"[c] - checkout\n[r] - return\n[x] - exit\n")
        option = input("Your Input: ").lower()
        if option == "c":
            print("Shipping Info: ")
            shippingAddress = getShippingAddress(state.user_state)
            option = ""
            if (shippingAddress):
                option = input(f"\tWould you like to ship to the address at {shippingAddress.street_one} [y]: ").lower()
            if (option != "y"):
                tempAddress = addressView()
                option = input("\tWould you like to save the new address [y]: ").lower()
                if (tempAddress and option == "y"):
                    updateShippingAddress(state.user_state, tempAddress)
                shippingAddress = tempAddress
            print("Payment Info: ")
            paymentOption = paymentView()
            if newOrderFromCart(cart, shippingAddress, paymentOption):
                resetUserCart(state.user_state)
        elif option == "r":
            return
        elif option == "x":
            sys.exit(0)
