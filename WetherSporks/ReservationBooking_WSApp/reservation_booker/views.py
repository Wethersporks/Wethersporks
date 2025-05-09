from django.shortcuts import render
from ..models import *

from ..BookingScheduler import BookingScheduler, BookingError


from typing import Union
import datetime



# API-Call Functions 

def reservation_deleter(request, resID):
    """ Reservation Booker / ReservationDeleter (Cancellation)
    Sent here through email """    

    # NOTE - This needs to be secured by adding a customer authentication before manipulating this reservation data
    bs = BookingScheduler()
    res = bs.cancel_reservation(Reservation.objects.filter(res_id = resID).first())
    content = {}

    if isinstance(res, BookingError):
        content.update({
            "error": res.msg
        })

    return render(request, "ReservationBooking/ReservationCancelled.html", content)
    



def reservation_selector(request):
    """ Reservation Booker / Reservation Selector Component """
 
    bs = BookingScheduler()

    content = {}

    if "time" in request.GET:
        time_selected = request.GET["time"]
        quantity = request.GET["guestCount"]
        date_selected = request.GET["date"]
        
        # Email from form is temp paused while devloping - Default email is inserted below
        _ = request.GET["email"]

        # Creating or selecting customer instance into database
        test_customer:Customer = Customer.objects.filter(name="Josh", number="0784921323", email="100715281@unimail.derby.ac.uk").first()
        if not test_customer:
            test_customer = Customer(name="Josh", number="0784921323", email="100715281@unimail.derby.ac.uk")
            test_customer.save()

        res = bs.append_reservation(test_customer, quantity, date_selected, time_selected)
        if isinstance(res, BookingError):
            content.update({
                "error": res.msg
            })


    elif "date" in request.GET:
        date_selected  = request.GET["date"]
        email_inputted = request.GET["email"]

        # Selects all time slots for this day if has free tables left over.
        available_timeslots = [ts.start_time.strftime("%H:%M") for ts in TimeSlot.objects.filter(start_date=date_selected) if (ts.tables.count() > 0)]
        
        
        content = {
            "date_selected":date_selected,
            "email_inputted":email_inputted,
            "timeslots":available_timeslots
        }


    
    return render(request, "ReservationBooking/ReservationSelector.html", content)

def dashboard(request):
    return render(request, 'Dashboard.html')

def booking(request):
    return render(request, 'ReservationSelector.html')

def welcome(request):
    return render(request, 'WElcomePage.html')

def contact(request):
    return render(request, 'ContactPage.html')

