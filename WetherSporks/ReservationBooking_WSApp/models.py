from django.db import models


# DJANGO MODEL - Module provides CRUD Operations for each MODEL! 
# Refer to Component Diagram for "Django Model CRUD"

class Table(models.Model):
    table_no = models.IntegerField()
    seat_count = models.IntegerField()

    def __str__(self):
        return f"{self.table_no} ({self.seat_count} seats)"


class TimeSlot(models.Model):      # TODO: Make factory for
    start_date = models.DateField()
    start_time = models.TimeField()
    duration = models.DurationField(null=False)
    tables = models.ManyToManyField("Table", through="TimeSlotTable")  # models.ForeignKey(Table, on_delete=models.CASCADE) #FK
    end_time = models.TimeField() # Needed for checking tables in time frame

    def occupy_table(self, table:Table):
        """ Takes table instances and removes from the available tables list """
        self.tables.remove(table)

    def unoccupy_table(self, table:Table):
        """ For cancellations - Re-appends table """
        self.tables.add(table)


class TimeSlotTable(models.Model):
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)


class Customer(models.Model):
    name = models.CharField(max_length=30)
    number = models.CharField(max_length=11)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class ResStatus(models.Model):
    status = models.CharField(max_length=9)


class Reservation(models.Model):    
    # res_id: Used for referencing in cancellations 
    res_id = models.AutoField(primary_key=True)

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) # FK
    guest_count = models.IntegerField(default=1)
    
    table = models.ForeignKey(Table, on_delete=models.CASCADE) #FK
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE) # FK
    status = models.ForeignKey(ResStatus, on_delete=models.CASCADE) #FK


    def __str__(self) -> str:
        return f"{self.customer} has booking for {self.guest_count} on table {self.table} \
                at {self.timeslot.start_date}-{self.timeslot.end_time}" 

    def __iter__(self):
        """ For casting to tuple in BookingScheduler.get_reservation_details """
        yield self.customer
        yield self.guest_count
        yield self.table
        yield self.timeslot
        yield self.status



