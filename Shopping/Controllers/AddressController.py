from Models import Address, PaymentInfo
from Helpers import getSession

def newAddress(street_one, street_two, city, state, zip) -> Address:
    session = getSession()
    addressInstance = Address(street_one=street_one, street_two=street_two, city=city, state=state, zip=zip)

    session.add(addressInstance)
    session.commit()

    session.refresh(addressInstance)
    return addressInstance

def deleteAddress(address: Address):
    session = getSession()
    session.query(Address).filter_by(address_id=address.address_id).delete()
    session.commit()
