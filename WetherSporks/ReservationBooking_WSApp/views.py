from django.shortcuts import render
from .models import *
from django.db.models import Min
from typing import Union
import datetime


class BookingScheduler:
    

    def get_available_table(self, date,time, quantity) -> Union[int, None]:
        """ Gets an available table ID from a timeslot given the seat quantity """

        timeslot = TimeSlot.objects.filter(start_date=date,
                                           start_time=time
                                           ).first()
        suitable_tables_in_timeslot = timeslot.tables.all().filter(seat_count__gte=int(quantity)) # USE .REMOVE() to remove table from timeslot on successful booking
        
        # Picks the table with the least seats - this table is suitable for the requested quantity & saves larger tables for other bookings (potentially larger bookings)
        most_suitable_table = suitable_tables_in_timeslot.filter().annotate(Min("seat_count")).order_by("seat_count")[0]
        print(most_suitable_table)


    def check_availability(self, date, time, quantity) -> bool:
        """ Determines if timeslot has availability given the seating quantity """
      
        timeslot = TimeSlot.objects.filter(start_date=date,
                                           start_time=time
                                           ).first()
        suitable_tables_in_timeslot = timeslot.tables.all().filter(seat_count__gte=int(quantity)) # USE .REMOVE() to remove table from timeslot on successful booking


        print(suitable_tables_in_timeslot)
        print(len(suitable_tables_in_timeslot))
        return len(suitable_tables_in_timeslot) != 0
    
        
        # tables_used_in_timeslot = TimeSlot.objects.filter(start_date__gte=date, 
        #                                                    start_time__gte=time, 
        #                                                    end_time__lte=end_time)

    




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

    bs = BookingScheduler()

    # Trigger time slot generation (time slots for today)
    #create_time_slots()


    if "time" in request.GET:
        time_selected = request.GET["time"]
        quantity = request.GET["guestCount"]
        date_selected = request.GET["date"]

        bs.get_available_table(date_selected, time_selected, quantity)
        bs.check_availability(date_selected, time_selected, quantity)
        

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