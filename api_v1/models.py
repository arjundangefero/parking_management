from django.db import models
from datetime import date
from django.core.exceptions import ValidationError


class ParkingRate(models.Model):
    rate = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"${self.rate}"

class ParkingSlot(models.Model):
    date = models.DateField()
    slot_number = models.IntegerField()
    is_available = models.BooleanField(default=True)
    time_slot_choices = (
        ('MORNING', '8 AM to 12 PM'),
        ('AFTERNOON', '12 PM to 6 PM'),
        ('EVENING', '6 PM to 12 AM'),
    )
    time_slot = models.CharField(max_length=20, choices=time_slot_choices)
    rates = models.ManyToManyField(ParkingRate, related_name='parking_slots')

    class Meta:
        unique_together = ('date', 'slot_number', 'time_slot')

    def __str__(self):
        return f"ParkingSlot {self.id} ({self.date}, Slot {self.slot_number}, {self.time_slot})"



class Customer(models.Model):
    name = models.CharField(max_length=255 , blank=True)
    contact_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    parking_slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE)
    booking_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('parking_slot', 'booking_date')

    def __str__(self):
        return f'{self.customer} - {self.parking_slot} - {self.booking_date}'
