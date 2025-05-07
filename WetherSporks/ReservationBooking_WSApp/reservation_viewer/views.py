from django.shortcuts import render
from ..models import (TimeSlot, Table, Customer, ResStatus, Reservation)
import datetime
from typing import Union
from .ModelInstanceCreator import ModelInstanceCreator
from ..BookingScheduler import (BookingScheduler, BookingError)






# VIEWS



# Trigger time slot generation (time slots for today)
def timeslot_generator(request):
    """ Create time-slots for today - Run at start of day """

    START_TIME = "10:00"
    CLOSE_TIME = "20:00" # This will generate 10 time slots for day 
    SLOT_DURATION_HOURS:float = 1.0

    open_time = datetime.datetime.combine(
        datetime.datetime.today().date(), datetime.datetime.strptime(START_TIME, "%H:%M").time())

    close_time = datetime.datetime.combine(
        datetime.datetime.today().date(), datetime.datetime.strptime(CLOSE_TIME, "%H:%M").time())

    open_duration = (close_time - open_time)
    hours_open_for = (open_duration.seconds/60)/60

    mic = ModelInstanceCreator() # mic the Factory provider - This is effectively a scalable version of 'TimeslotCreator'

    timeslots:list = []
    for i in range(int(hours_open_for)):
        # TimeSlot for each hour
        timeslot_offset = datetime.timedelta(hours=SLOT_DURATION_HOURS*i)
        timeslots_datetime = open_time + timeslot_offset
        timeslot:TimeSlot = mic.timeslot_factory(timeslots_datetime, SLOT_DURATION_HOURS)
        timeslots.append(timeslot)

    print("Created timeslots today")

    return render(request, "Reservationviewing/TimeslotGenerator.html", {
        "start":open_time, "end":close_time, "timeslots":timeslots 
    })


def reservation_updater(request, resID):
    """ Bookings Handler / Bookings Updater """

    reservation = Reservation.objects.filter(res_id = resID).first()
    content = {}
    if reservation:
        bs = BookingScheduler()


        if "new_date" in request.GET:
            content.update({"reservation_details": bs.get_reservation_details(reservation)})
        
            res = bs.update_reservation(
                reservation, 
                request.GET["new_date"],
                request.GET["new_time"],
                request.GET["guest_count"]
                )
        
        
        content.update({
            "start_date": str(datetime.datetime.strftime(reservation.timeslot.start_date, "%Y-%m-%d")), 
            "start_time": str(reservation.timeslot.start_time.strftime("%H:%M:%S")), 
            "guest_count": reservation.guest_count
            })


    return render(request, "Reservationviewing/ReservationUpdater.html", content)


def dashboard(request):
    """ Bookings Handler / Bookings Dashboard """
    date:datetime.datetime

    if "date" in request.GET and request.GET["date"] != "":
        date = datetime.datetime.strptime(request.GET["date"], "%Y-%m-%d")
    else:
        date = datetime.datetime.today()
    # Each timeslot passed into template is in Tuple (TimeSlot Instance, [Timeslots tables instances], [Timeslots Reservation Instances])
    data = [(
                ts, 
                ts.tables.all(), 
                Reservation.objects.filter(timeslot=ts)
            )
            for ts in TimeSlot.objects.filter(start_date=date)]

     
    # localhost:8000/reservation/book/cancel/6

    return render(request, "Reservationviewing/Dashboard.html", {"timeslots":data, "date":date})