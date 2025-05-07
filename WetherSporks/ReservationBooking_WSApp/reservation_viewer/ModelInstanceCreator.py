from ..models import (TimeSlot, Table)
import datetime
from typing import Union

class ModelInstanceCreator:
    """ Generates user-defined django model instances - each factory takes related parameters for its model """
    
    DEFAULT_DURATION_HOURS = 1
    
    def __init__(self):
        """"""
        pass


    def timeslot_factory(self, start_time:datetime.datetime, duration:float) -> Union[TimeSlot, None]:
        """ Factory - Creates a TimeSlot & sets relationship with tables. """

        duration = datetime.timedelta(hours=duration)
        end_time = start_time + duration

        # Test if timeslot already exist
        time_slot:Union[TimeSlot, None] = TimeSlot.objects.filter(start_date=start_time.date(), start_time=start_time.time())
        if time_slot:
            print("Time slot already exists")
            return None


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
        