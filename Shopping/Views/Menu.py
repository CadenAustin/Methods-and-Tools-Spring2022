import sys
from Controllers import getAllBooks, getAllMovies
import Helpers.state as state

from .Account import accountView
from .Order import orderView
from .Store import storeView


def menuView():
    while 1:
        print(f"\nWelcome {state.user_state.username if len(state.user_state.name) == 0 else state.user_state.name} to our shopping application!")
        print("Please Select From The Following Options:\n[s] - access the store\n[a] - manage your account\n[o] - view your previous orders\n[l] - Logout\n[x] - Exit\n")
        option = input("Your Input: ").lower()
        if option == "s":
            storeView()
        elif option == "a":
            if (accountView()):
                return
        elif option == "o":
            orderView()
        elif option == "l":
            state.user_state = None
            return
        elif option == "x":
            sys.exit(0)