from django.shortcuts import render
from .models import *

from typing import Union
import datetime


class BookingScheduler:
    

    def check_availability(self, date, time, quantity, tableNo:int) -> bool:
        """ """
      
        start_datetime = datetime.datetime.combine(date, time)


        duration=datetime.timedelta(hours=self.DEFAULT_DURATION_HOURS)
        end_time = start_datetime + duration
        
        tables_used_in_timeslot = TimeSlot.objects.filter(start_date__gte=date, 
                                                           start_time__gte=time, 
                                                           end_time__lte=end_time)

        
        print(tables_used_in_timeslot)
        for tbl in list(tables_used_in_timeslot):
            print(f"Table: {tbl.table}; is in use - at {tbl.start_date} {tbl.start_time} for {tbl.duration}")



    def get_available_table(self, date:str, time:str, quantity) -> Union[int, None]:
        """ Returns table ID if available, else returns None if none avaiable """
        
        slot_has_availability = self.check_availability(start_date[0], start_time[0], quantity)

        suitable_tables = Table.objects.filter(seat_count__gte=int(quantity))
        



class ModelInstanceCreator:
    """ Generates user-defined django model instances - each factory takes related parameters for its model """
    
    DEFAULT_DURATION_HOURS = 1
    
    def __init__(self):
        pass


    def timeslot_factory(self, start_time:datetime.datetime, duration:float) -> Union[TimeSlot, None]:
        """ Factory - Creates a TimeSlot & sets relationship with tables. """

        duration = datetime.timedelta(hours=duration)
        end_time = start_time + duration


        print(start_time) 
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

        print(timeslot.tables.all())
        return TimeSlot
        



def create_time_slots():
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





def index(request):
    """ Home-Page """
    f = ModelInstanceCreator()


    # Trigger time slot generation (time slots for today)
    create_time_slots()


    if "time" in request.GET:
        time_selected = request.GET["time"]
        quantity = request.GET["guestCount"]
        date_selected = request.GET["date"]

        print(f"Time Picked: {time_selected} for {quantity} people on {date_selected}")
        
        # Reservation ready to make
        blank_customer = Customer(name="Josh", number="0784921323", email="Joshhhhh@gmail.com")

        blank_customer.save()
        reservation = Reservation(
            guest_count = quantity,
            
            customer = blank_customer,

            start_time = f.timeslot_factory(date_selected, time_selected, quantity),

            status = ResStatus.objects.get(status="Pending")
        )
        reservation.save()


    elif "date" in request.GET:
        date_selected = request.GET["date"]
        return render(request, "ReservationBooking/Index.html", {"date_selected":date_selected})



    return render(request, "ReservationBooking/Index.html")