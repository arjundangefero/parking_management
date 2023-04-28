from rest_framework import serializers
from .models import ParkingSlot, Booking


class ParkingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSlot
        fields = ['id', 'date', 'is_available', 'time_slot']


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'parking_slot', 'customer', 'booking_date')
        read_only_fields = ('id', 'booking_date')