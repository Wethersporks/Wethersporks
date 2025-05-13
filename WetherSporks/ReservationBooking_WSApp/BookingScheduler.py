from typing import Union
from .models import (TimeSlot, Table, Customer, ResStatus, Reservation)
from django.db.models import Min # type: ignore
from .reservation_booker.emailer import send_email



class BookingError:
    def __init__(self, msg):
        self.msg = msg

class BookingScheduler(object):
    
    def __new__(cls):
        """ SINGLETON FUNCTIONALITY """
        if not hasattr(cls, "instance"):
            print("[BOOKING SCHEDULER]: Creating ONE instance of BookingScheduler")
            cls.instance = super(BookingScheduler, cls).__new__(cls)
        else:
            print("[BOOKING SCHEDULER] Instance already created")
        return cls.instance




    def __get_timeslot(self, date,time) -> Union[TimeSlot, None]:
        """ Returns timeslot within given date & time """
        return TimeSlot.objects.filter(start_date=date,
                                start_time=time
                                ).first()

    def get_available_table(self, quantity, time_slot=Union[TimeSlot, None], date:Union[str, None]=None, time=Union[str, None]) -> Union[Table, BookingError]:
        """ Gets the most suitable Table Instance from a timeslot given the seat quantity """

        if not time_slot:
            if date and time:
                time_slot = TimeSlot.objects.filter(start_date=date,
                                                    start_time=time).first()
            else:
                return BookingError("Must specify either date string or a timeslot instance")
        
        time_slot_tables = time_slot.tables.all()
        suitable_tables_in_timeslot = time_slot_tables.filter(seat_count__gte=int(quantity)) # USE .REMOVE() to remove table from timeslot on successful booking

        # Picks the table with the least seats - this table is suitable for the requested quantity & saves larger tables for other bookings (potentially larger bookings)
        most_suitable_table = suitable_tables_in_timeslot.filter().annotate(Min("seat_count")).order_by("seat_count").first()
        return most_suitable_table


    def check_availability(self, date, time, quantity) -> bool:
        """ Determines if timeslot has availability given the seating quantity """
      
        timeslot = TimeSlot.objects.filter(start_date=date,
                                           start_time=time
                                           ).first()
        suitable_tables_in_timeslot = timeslot.tables.all().filter(seat_count__gte=int(quantity))

        return len(suitable_tables_in_timeslot) != 0
    


    def append_reservation(self, customer:Customer, guest_count, date, time) -> Union[BookingError, None]:
        time_slot:TimeSlot = self.__get_timeslot(date, time)
        
        if time_slot:
            if Reservation.objects.filter(customer=customer, timeslot=time_slot).first():
                # Reservation already made under this customer at this time
                return BookingError(f"{customer} has already made reservation at {time_slot}")

            print(f"{time_slot} at {time_slot.start_time}-{time_slot.end_time} \
                  \nhas {time_slot.tables.count()} tables: {time_slot.tables.all()}")
            
            table:Table      = self.get_available_table(guest_count, time_slot=time_slot)
            if table:
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

                EMAILING_SYSTEM_ON = False
                if EMAILING_SYSTEM_ON:
                    send_email(customer.email, 
                            data=f"""Your reservation has been booked! 
                            To cancel: localhost:8000/reservation/book/cancel/{reservation.res_id}
                            """,
                            subject="WetherSporks Reservation Booking"
                            )
                print(f"to cancel go to 'localhost:8000/reservation/book/cancel/{reservation.res_id}'")

                print(f"[{self.append_reservation.__name__}]: Successfully saved reservation")
            else:
                # Availability Checker - REFER TO COMPONENT DIAGRAM
                return BookingError(f"No Available Tables Found {date} - {time} doesnt exist")
                
        else:
            # Timeslot not generated in system 
            return BookingError(f"Time slot at {date} - {time} doesnt exist")
            

    def update_reservation(self, reservation:Reservation, new_date, new_time, guest_count:int=0) -> Union[BookingError, None]:
        """ Update timeslot and/or guest count for an existing reservation """
        if reservation:
            new_timeslot:TimeSlot = self.__get_timeslot(new_date, new_time)
            if new_timeslot:
                reservation.timeslot.unoccupy_table(reservation.table)
                table:Table = self.get_available_table(int(guest_count), new_timeslot)
                reservation.table = table
                new_timeslot.occupy_table(table)
                new_timeslot.save()
                reservation.timeslot = new_timeslot

            else:
                return BookingError(f"Timeslot doesn't exist for {new_date} {new_time}")
            if guest_count != 0:
                # Request to change guest_count
                # Cannot have a guest count of 0. This is default for this function call so doesn't need to be specified (may only change timeslot)
                reservation.guest_count = int(guest_count)
            reservation.save()
        else:
            return BookingError("reservation doesnt exist")


    def cancel_reservation(self, reservation:Union[Reservation,None]) -> Union[BookingError, None]:
        """ Takes Reservation Instance - Changes reservation status to 'Cancelled' & re-adds table to appropriate timeslot """
        if reservation:
            reservation.status = ResStatus.objects.filter(status="Cancelled").first()
            reservation.save()
            reservation.timeslot.tables.add(reservation.table)
        else:
            return BookingError("Reservation Doesnt Exist")


    def get_reservation_details(self, reservation:Reservation) -> tuple:
        return tuple(reservation)
