from django.contrib import admin
from .models import *


# Register your models here.

admin.site.register(Tables)
admin.site.register(TimeSlots)
admin.site.register(Customers)
admin.site.register(ResStatuses)
admin.site.register(Reservations)