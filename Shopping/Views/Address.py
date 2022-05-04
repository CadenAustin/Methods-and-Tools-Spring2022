from Controllers import newAddress

def addressView():
    street_one = input("\tStreet Address: ")
    street_two = input("\tStreet Address 2: ")
    city = input("\tCity: ")
    state = input("\tState(ex MS): ").lower()
    try:
        zip = int(input("\tZip: "))
    except:
        print("Zip must be a number. Returning now.")
        return None

    address = newAddress(street_one, street_two, city, state, zip)
    if address:
        return address
    return None
