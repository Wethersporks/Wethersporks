from django.shortcuts import render
from ..models import *
from ..BookingScheduler import BookingScheduler


from typing import Union
import datetime






# API-Call Functions 

def cancel_reservation(request, resID):
    """ Sent here through email """    
    # NOTE - This needs to be secured by adding a customer authentication before manipulating this reservation data
    bs = BookingScheduler()
    bs.cancel_reservation(Reservation.objects.filter(res_id = resID).first())

    print(f"cancelling reservation: {resID}")



def availability(request):
    pass



def index(request):
    """ Home-Page """
 

    bs = BookingScheduler()


    if "time" in request.GET:
        time_selected = request.GET["time"]
        quantity = request.GET["guestCount"]
        date_selected = request.GET["date"]
        _ = request.GET["email"]


        # Keeping the customer creation for scalability
        test_customer:Customer = Customer.objects.filter(name="Josh", number="0784921323", email="100715281@unimail.derby.ac.uk").first()
        if not test_customer:
            test_customer = Customer(name="Josh", number="0784921323", email="100715281@unimail.derby.ac.uk")
            test_customer.save()

        bs.append_reservation(test_customer, quantity, date_selected, time_selected)

    


    elif "date" in request.GET:
        date_selected  = request.GET["date"]
        email_inputted = request.GET["email"]
        return render(request, "ReservationBooking/Index.html",
                       {"date_selected":date_selected,
                        "email_inputted":email_inputted
                        })



    return render(request, "ReservationBooking/Index.html")