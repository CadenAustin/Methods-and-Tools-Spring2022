import sys
from .Cart import cartView
from .Table import tableView, createHeaders
from Controllers import getAllBooks, getAllMovies, getUserCart, updateCartItem, getCurrentCartQuantity
from Helpers import flattenEntries
import Helpers.state as state

def storeView():
    books = getAllBooks()
    movies = getAllMovies()
    while 1:
        print("Please Select From The Following Options:\n[b] - view our books\n[m] - view our movies\n[t] - search by title\n[a] - add an item to your cart\n[c] - manage and view your cart\n[r] - return\n[x] - Exit\n")
        option = input("Your Input: ").lower()
        if option == "b":
            if(len(books) > 0):
                flatBooks = flattenEntries(books)
                headers = createHeaders(["title", "author", "genre", "publisher", "price", "inv_quantity"])
                tableView(headers, flatBooks, index = True)

        elif option == "m":
            if(len(movies) > 0):
                flatMovies = flattenEntries(movies)
                headers = createHeaders(["title", "director", "leading_actor", "genre", "price", "inv_quantity"])
                tableView(headers, flatMovies, index = True)

        elif option == "t":
            title = input("\tWhat title would you like to search for: ").lower()
            flatBooks = flattenEntries(books)
            results = [{**{"#": index}, **item} for index, item in enumerate(flatBooks) if title in item["title"].lower()]
            flatMovies = flattenEntries(movies)
            movieResults = [{**{"#": index}, **item} for index, item in enumerate(flatMovies) if title in item["title"].lower()]
            if (movieResults):
                results.extend(movieResults)
            headers = createHeaders(["#", "item_type", "title", "genre", "price", "inv_quantity"])
            tableView(headers, results, index = False)


        elif option == "a":
            cart = getUserCart(state.user_state)
            if not cart:
                print("There was a problem retrieving your cart")
                continue
            itemType = input("\tWould you like to add a [b]ook or [m]ovie: ").lower()
            if itemType not in ["b", "m"]:
                print("Invalid type please enter b/m")
                continue
            try:
                itemIndex = int(input(f"\tPlease enter the number for the {'book' if itemType == 'b' else 'movie'} you'd like to add to your cart: "))
                if itemType == "b":
                    item = books[itemIndex]
                elif itemType == "m":
                    item = movies[itemIndex]
            except:
                print(f"There is no {'book' if itemType == 'b' else 'movie'} #{itemIndex}")
                continue
            try:
                itemQuantity = int(input(f"\tHow many {item.InventoryItem.title}s would you like to purchase: "))
            except:
                print("Item quantity must be an integer.")
                continue
            if itemQuantity < 0 or itemQuantity > item.InventoryItem.inv_quantity:
                print(f"We're sorry but that's an invalid number of items. We currently have {item.InventoryItem.inv_quantity} of {item.InventoryItem.title} in our inventory.")
                continue
            cartQuantity = getCurrentCartQuantity(cart, item.InventoryItem)
            updateCartItem(cart, item, itemQuantity+cartQuantity)
            if itemType == "b":
                books = getAllBooks()
            elif itemType == "m":
                movies = getAllMovies()

        elif option == "c":
            cartView()
            books = getAllBooks()
            movies = getAllMovies()
        elif option == "r":
            return
        elif option == "x":
            sys.exit(0)