import datetime

from Controllers import attatchAddressToPayment, attatchPaymentInfoToUser, getPaymentInfo, newPaymentInfo
from Controllers.PaymentController import deletePaymentInfo
import Helpers.state as state
from Models import PaymentInfo
from .Address import addressView


def paymentView() -> PaymentInfo:
    paymentInfo = getPaymentInfo(state.user_state)
    if paymentInfo:
        option = input(f"\tWould you like to use the card ending in {paymentInfo.card_number[-4:]} y/n: ").lower()
        if option == 'y':
            return paymentInfo
        elif option != 'n':
            print("Invalid selection returning to previous menu.")
            return None

    card_number = input("\tCard Number: ")
    try:
        cvv = int(input("\tCVV: "))
    except:
        print("CVV should be a number, returning to previous menu.")
        return None
    try:
        expiration_month = int(input("\tExpiration Month: "))
        expiration_year = int(input("\tExpiration Year: "))
        expiration = datetime.date(year=expiration_year, month=expiration_month, day=1)
    except:
        print("Month and Year should be in numercal form.")
        return None

    print("Billing Address: ")
    billingAddress = addressView()
    if billingAddress:
        createdPaymentInfo = newPaymentInfo(card_number, cvv, expiration)
        if createdPaymentInfo:
            attatchAddressToPayment(createdPaymentInfo, billingAddress)
            option = input(f"Would you like to save this payment info to your account [y]: ").lower()
            if option == "y":
                attatchPaymentInfoToUser(state.user_state, createdPaymentInfo)
                if paymentInfo:
                    deletePaymentInfo(paymentInfo)
            
            return createdPaymentInfo
    
    print("Invalid Billing Address.")
    return None


