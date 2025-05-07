from typing import Union
from .models import (TimeSlot, Table, Customer, ResStatus, Reservation)
from django.db.models import Min
from .reservation_booker.emailer import send_email



class BookingError:
    def __init__(self, msg):
        self.msg = msg

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
        suitable_tables_in_timeslot = timeslot.tables.all().filter(seat_count__gte=int(quantity)) # USE .REMOVE() to remove table from timeslot on successful booking


        print(suitable_tables_in_timeslot)
        print(len(suitable_tables_in_timeslot))
        return len(suitable_tables_in_timeslot) != 0
    


    def append_reservation(self, customer:Customer, guest_count, date, time) -> Union[BookingError, None]:
        time_slot:TimeSlot = self.get_timeslot(date, time)
        
        if time_slot:
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
                return BookingError(f"No Available Tables Found {date} - {time} doesnt exist")
                
        else:
            # Timeslot not generated in system 
            return BookingError(f"Time slot at {date} - {time} doesnt exist")
            

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
        """ Takes Reservation Instance - Changes reservation status to 'Cancelled' & re-adds table to appropriate timeslot """
        if reservation:
            reservation.status = ResStatus.objects.filter(status="Cancelled").first()
            reservation.save()
            reservation.timeslot.tables.add(reservation.table)
        else:
            print(f"[{self.update_reservation.__name__}]: Reservation NOT FOUND")


    def get_reservation_details(self, reservation:Reservation) -> tuple:
        return tuple(reservation)
