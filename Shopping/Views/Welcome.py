from .Login import loginView
from .Register import registerView

def welcomeView():
    while 1:
        print("Please Select From The Following Options:\n[l] - Login\n[r] - Register\n[x] - Exit\n")
        option = input("Your Input: ").lower()
        if option == "l":
            loginView()
        elif option == "r":
            registerView()
        elif option == "x":
            return