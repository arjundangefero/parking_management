from django.contrib import admin
from .models import ParkingSlot, Booking , Customer , ParkingRate
# Register your models here


admin.site.register(ParkingSlot)
admin.site.register(Booking)
admin.site.register(Customer)
admin.site.register(ParkingRate)