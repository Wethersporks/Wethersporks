from django.shortcuts import render
from .models import *

from typing import Union
import datetime


class BookingScheduler:
    DEFAULT_DURATION_HOURS = 1

    def check_availability(self, date:datetime._Date, time:datetime._Time, quantity, tableNo:int) -> bool:
        """ """
      
        start_datetime = datetime.datetime.combine(date, time)


        duration=datetime.timedelta(hours=self.DEFAULT_DURATION_HOURS)
        end_time = start_datetime + duration
        
        tables_used_in_timeslot = TimeSlots.objects.filter(start_date__gte=date, 
                                                           start_time__gte=time, 
                                                           end_time__lte=end_time)

        
        print(tables_used_in_timeslot)
        for tbl in list(tables_used_in_timeslot):
            print(f"Table: {tbl.table}; is in use - at {tbl.start_date} {tbl.start_time} for {tbl.duration}")



    def get_available_table(self, date:str, time:str, quantity) -> Union[int, None]:
        """ Returns table ID if available, else returns None if none avaiable """
        
        suitable_tables = Tables.objects.filter(seat_count__gte=int(quantity))
        for 



class ModelInstanceCreator:
    """ Generates user-defined django model instances - each factory takes related parameters for its model """
    
    
    def __init__(self):
        pass


    def timeslot_factory(self, date:str, time:str, quantity:int) -> Union[TimeSlots, None]:
        bs = BookingScheduler()

        start_date=datetime.datetime.strptime(date, "%Y-%m-%d").date(), 
        start_time=datetime.datetime.strptime(time, "%H:%M").time(), 
        
        slot_has_availability = bs.check_availability(start_date[0], start_time[0], quantity)


        
        if len(tables) != 0:
            for table in tables:    
                print(f"tableno:{table.table_no} seatcount:{table.seat_count}") 
                if table 


#        print(tables)
        #print(f"Your table number is: {tables.first().table_no}")

       # print(len(tables))


        time_slot = TimeSlots(
            start_date=date, 
            start_time=time, 
            duration=duration,
            table=tables.first(),
            end_time = end_time
            )
        time_slot.save()
        return time_slot



def index(request):
    """ Home-Page """
    f = ModelInstanceCreator()

    if "time" in request.GET:
        time_selected = request.GET["time"]
        quantity = request.GET["guestCount"]
        date_selected = request.GET["date"]

        print(f"Time Picked: {time_selected} for {quantity} people on {date_selected}")
        
        # Reservation ready to make
        blank_customer = Customers(name="Josh", number="0784921323", email="Joshhhhh@gmail.com")

        blank_customer.save()
        reservation = Reservations(
            guest_count = quantity,
            
            customer = blank_customer,

            start_time = f.timeslot_factory(date_selected, time_selected, quantity),

            status = ResStatuses.objects.get(status="Pending")
        )
        reservation.save()


    elif "date" in request.GET:
        date_selected = request.GET["date"]
        return render(request, "ReservationBooking/Index.html", {"date_selected":date_selected})



    return render(request, "ReservationBooking/Index.html")