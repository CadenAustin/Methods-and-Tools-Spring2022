import sys

from Controllers import getItemsInCart, getShippingAddress, getUserCart, newOrderFromCart, updateShippingAddress, updateCartItem, getCurrentCartQuantity, resetUserCart, getCartItem
import Helpers.state as state
from Helpers import flattenEntries
from .Payment import paymentView
from .Address import addressView
from .Table import tableView, createHeaders

def cartView():
    while 1:
        cart = getUserCart(state.user_state)
        cartItems = getItemsInCart(cart)
        flatBooks = flattenEntries(cartItems["books"])
        flatMovies = flattenEntries(cartItems["movies"])
        table = flatBooks if flatBooks else []
        if flatMovies:
            table.extend(flatMovies)
        headers = createHeaders(["title", "item_quantity", "price", "subtotal", "item_type"])
        tableView(headers, table, index=True)
        print(f"\nYour current total is ${cart.total:.2f}\n")
        print(f"[c] - checkout\n[e] - remove item from cart\n[q] - modify the quantity of an item in cart\n[r] - return\n[x] - exit\n")
        option = input("Your Input: ").lower()
        if option == "c":
            print("Shipping Info: ")
            shippingAddress = getShippingAddress(state.user_state)
            option = ""
            if (shippingAddress):
                option = input(f"\tWould you like to ship to the address at {shippingAddress.street_one + ' ' + shippingAddress.street_two} [y]: ").lower()
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
        elif option == "e":
            try:
                itemIndex = int(input("\tWhat item would you like to remove: "))
                cart_item_id = table[itemIndex]["cart_item_id"]
                item = getCartItem(cart_item_id)
                updateCartItem(cart, item, 0)
            except:
                print("Invalid Item Index.")
                continue
        elif option == "q":
            try:
                itemIndex = int(input("\tWhat item would you like to change: "))
                cart_item_id = table[itemIndex]["cart_item_id"]
                item = getCartItem(cart_item_id)
                itemQuantity = int(input(f"\tHow many {item.title} would you like: "))
                cartQuantity = getCurrentCartQuantity(cart, item)
                if itemQuantity < 0 or itemQuantity > item.inv_quantity + cartQuantity:
                    print(f"Invalid ammount of items. We currently only have {item.inv_quantity + cartQuantity} left.")
                    continue
                updateCartItem(cart, item, itemQuantity)
            except:
                print("Invalid Item Options.")
                continue
        elif option == "r":
            return
        elif option == "x":
            sys.exit(0)
