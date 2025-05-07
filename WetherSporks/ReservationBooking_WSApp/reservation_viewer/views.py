from django.shortcuts import render
from ..models import *
import datetime
from typing import Union






class ModelInstanceCreator:
    """ Generates user-defined django model instances - each factory takes related parameters for its model """
    
    DEFAULT_DURATION_HOURS = 1
    
    def __init__(self):
        pass


    def timeslot_factory(self, start_time:datetime.datetime, duration:float) -> Union[TimeSlot, None]:
        """ Factory - Creates a TimeSlot & sets relationship with tables. """

        duration = datetime.timedelta(hours=duration)
        end_time = start_time + duration
     
        # Create Timeslot instance
        timeslot:TimeSlot = TimeSlot(
            start_date=start_time.date(),
            start_time=start_time.time(),
            duration=duration,
            end_time = end_time
        )
        # Saves timeslot into DB
        timeslot.save()

        # Relationship between a time-slot and all tables
        tables = Table.objects.all()
        timeslot.tables.set(tables)

        return timeslot
        


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


    for i in range(int(hours_open_for)):
        # TimeSlot for each hour
        timeslot_offset = datetime.timedelta(hours=SLOT_DURATION_HOURS*i)
        timeslots_datetime = open_time + timeslot_offset
        timeslot:TimeSlot = mic.timeslot_factory(timeslots_datetime, SLOT_DURATION_HOURS)

    print("Created timeslots today")



def reservation_updater(request, resID):
    pass

def dashboard(request):

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
    
    # timeslots = TimeSlot.objects.filter(start_date=date)
     
    # localhost:8000/reservation/book/cancel/6

    return render(request, "Reservationviewing/Dashboard.html", {"timeslots":data, "date":date})