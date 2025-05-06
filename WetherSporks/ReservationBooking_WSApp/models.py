from django.db import models

#PREFIXING ALL MODELS WITH M_

class Table(models.Model):
    table_no = models.IntegerField()
    seat_count = models.IntegerField()


class TimeSlot(models.Model):      # TODO: Make factory for
    start_date = models.DateField()
    start_time = models.TimeField()
    duration = models.DurationField(null=False)
    tables = models.ManyToManyField("Table", through="TimeSlotTable")  # models.ForeignKey(Table, on_delete=models.CASCADE) #FK
    end_time = models.TimeField() # Needed for checking tables in time frame


class TimeSlotTable(models.Model):
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)


class Customer(models.Model):
    name = models.CharField(max_length=30)
    number = models.CharField(max_length=11)
    email = models.CharField(max_length=50)

class ResStatus(models.Model):
    status = models.CharField(max_length=9)


class Reservation(models.Model):    
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE) # FK
    guest_count = models.IntegerField(default=1)
    
    timeslot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE) # FK
    status = models.ForeignKey(ResStatus, on_delete=models.CASCADE) #FK




