from django.db import models

#PREFIXING ALL MODELS WITH M_

class Tables(models.Model):
    table_no = models.IntegerField()
    seat_count = models.IntegerField()

class TimeSlots(models.Model):      # TODO: Make factory for
    start_date = models.DateField()
    start_time = models.TimeField()
    duration = models.DurationField(null=False)
    table = models.ForeignKey(Tables, on_delete=models.CASCADE) #FK
    end_time = models.TimeField() # Needed for checking tables in time frame

class Customers(models.Model):
    name = models.CharField(max_length=30)
    number = models.CharField(max_length=11)
    email = models.CharField(max_length=50)

class ResStatuses(models.Model):
    status = models.CharField(max_length=9)


class Reservations(models.Model):    
    customer = models.ForeignKey(Customers, on_delete=models.CASCADE) # FK
    guest_count = models.IntegerField(default=1)
    
    timeslot = models.ForeignKey(TimeSlots, on_delete=models.CASCADE) # FK
    status = models.ForeignKey(ResStatuses, on_delete=models.CASCADE) #FK




