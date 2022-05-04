import sys

from sqlalchemy import true

from Controllers import getAllOrders, getAllItemsOnOrder
import Helpers.state as state
from Helpers import flattenEntries
from .Table import tableView, createHeaders

def orderView():
    hideTable = False
    while 1:
        orders = getAllOrders(state.user_state)
        flatOrders = flattenEntries(orders)
        headers = createHeaders(["total", "street_one", "street_two", "city"])
        if not hideTable and flatOrders:
            tableView(headers, flatOrders, index=True) 
        print("\nPlease Select From The Following Options:\n[v] - view a specific order\n[r] - Return\n[x] - Exit\n")
        option = input("Your Input: ").lower()
        if option == "v":
            try:
                orderNumber = int(input("\tWhich order would you like to view: "))
                orderItems = getAllItemsOnOrder(orders[orderNumber][0])
                flatBooks = flattenEntries(orderItems["books"])
                flatMovies = flattenEntries(orderItems["movies"])
                table = flatBooks if flatBooks else []
                if flatMovies:
                    table.extend(flatMovies)
                headers = createHeaders(["title", "item_quantity", "price", "subtotal", "item_type"])
                tableView(headers, table, index=True)
                hideTable = True
            except:
                print("Invalid Order Number.")
            continue
            
        elif option == "r":
            return
        elif option == "x":
            sys.exit(0)
        hideTable = False
