from django.shortcuts import render
from .models import *
from django.db.models import Min
from typing import Union
import datetime


class BookingScheduler:
    
    def get_timeslot(self, date,time) -> Union[TimeSlot, None]:
        """ Returns timeslot within given date & time """
        return TimeSlot.objects.filter(start_date=date,
                                start_time=time
                                ).first()
        # tables_used_in_timeslot = TimeSlot.objects.filter(start_date__gte=date, start_time__gte=time, end_time__lte=end_time)


    def get_available_table(self, quantity, time_slot=Union[TimeSlot, None], date:Union[str, None]=None, time=Union[str, None]) -> Union[Table, None]:
        """ Gets an available Table Instance from a timeslot given the seat quantity """

        if not time_slot:
            if date and time:
                time_slot = TimeSlot.objects.filter(start_date=date,
                                                start_time=time
                        ).first()
            else:
                print("[get_available_table]: MUST SPECIFY EITHER DATE STRING OR A TIMESLOT INSTANCE")
                return None
        
        suitable_tables_in_timeslot = time_slot.tables.all().filter(seat_count__gte=int(quantity)) # USE .REMOVE() to remove table from timeslot on successful booking

        # Picks the table with the least seats - this table is suitable for the requested quantity & saves larger tables for other bookings (potentially larger bookings)
        most_suitable_table = suitable_tables_in_timeslot.filter().annotate(Min("seat_count")).order_by("seat_count").first()
        return most_suitable_table


    def check_availability(self, date, time, quantity) -> bool:
        """ Determines if timeslot has availability given the seating quantity """
      
        timeslot = TimeSlot.objects.filter(start_date=date,
                                           start_time=time
                                           ).first()
        suitable_tables_in_timeslot = timeslot.tables.all().filter(seat_count__gte=int(quantity)) # USE .REMOVE() to remove table from timeslot on successful booking


        print(suitable_tables_in_timeslot)
        print(len(suitable_tables_in_timeslot))
        return len(suitable_tables_in_timeslot) != 0
    


    def append_reservation(self, customer:Customer, guest_count, date, time) -> None:
        time_slot:TimeSlot = self.get_timeslot(date, time)
        
        if time_slot:
            print(f"{time_slot} at {time_slot.start_time}-{time_slot.end_time} \
                  \nhas {time_slot.tables.count()} tables: {time_slot.tables.all()}")
            
            table:Table      = self.get_available_table(guest_count, time_slot=time_slot)
            status:ResStatus = ResStatus.objects.filter(status="Pending").first()

            reservation = Reservation(
                customer    = customer,
                guest_count = guest_count,
                table       = table,
                timeslot    = time_slot,
                status      = status
                )
            reservation.save()
            time_slot.occupy_table(table)
            time_slot.save()

            print(f"[{self.append_reservation.__name__}]: Successfully saved reservation")

        else:
            # Timeslot not generated in system 
            print(f"Time slot at {date} - {time} doesnt exist")

    def update_reservation(self, reservation:Reservation, new_date, new_time, guest_count:int=0) -> None:
        """ Update timeslot and/or guest count for an existing reservation """
        new_timeslot:TimeSlot = self.get_timeslot(new_date, new_time)
        if new_timeslot:
            reservation.timeslot = new_timeslot
        else:
            print(f"[{self.update_reservation.__name__}]: Timeslot doesn't exist for {new_date} {new_time}")
            return
        if guest_count != 0:
            # Request to change guest_count
            # Cannot have a guest count of 0. This is default for this function call so doesn't need to be specified (may only change timeslot)
            reservation.guest_count = guest_count
        reservation.save()


    def cancel_reservation(self, reservation:Reservation) -> None:
        # TODO Need to take table out of reservation and put it back in timeslots available tables
        reservation.status = ResStatus.objects.filter(status="Cancelled").first()
        reservation.timeslot.tables.add(reservation.table)
        


    def get_reservation_details(self, reservation:Reservation) -> tuple:
        return tuple(reservation)




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
        return timeslot
        



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




# API-Call Functions 

def cancel_reservation(request, resID):
    """ Sent here through email """    
    print(f"cancelling reservation: {resID}")



def index(request):
    """ Home-Page """
    f = ModelInstanceCreator()

    bs = BookingScheduler()


    if "time" in request.GET:
        time_selected = request.GET["time"]
        quantity = request.GET["guestCount"]
        date_selected = request.GET["date"]
        email = request.GET["email"]

        # Keeping the customer creation for scalability
        blank_customer:Customer = Customer.objects.filter(name="Josh", number="0784921323", email=email).first()
        blank_customer.save()
        bs.append_reservation(blank_customer, quantity, date_selected, time_selected)

        
        if False:

            bs.get_available_table(date_selected, time_selected, quantity)
            bs.check_availability(date_selected, time_selected, quantity)
            
            print(f"Time Picked: {time_selected} for {quantity} people on {date_selected}")
            
            # Reservation ready to make

            blank_customer.save()
            reservation = Reservation(
                guest_count = quantity,
                
                customer = blank_customer,

                start_time = f.timeslot_factory(date_selected, time_selected, quantity),

                status = ResStatus.objects.get(status="Pending")
            )
            reservation.save()


    elif "date" in request.GET:
        date_selected  = request.GET["date"]
        email_inputted = request.GET["email"]
        return render(request, "ReservationBooking/Index.html",
                       {"date_selected":date_selected,
                        "email_inputted":email_inputted
                        })



    return render(request, "ReservationBooking/Index.html")