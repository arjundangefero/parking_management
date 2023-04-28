from rest_framework import viewsets, permissions, status
from rest_framework import generics, status, filters
from .models import ParkingSlot
from .serializers import ParkingSlotSerializer, BookingSerializer
from .models import ParkingSlot, Booking, Customer
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count, Sum
from .serializers import MyTokenObtainPairSerializer
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class ParkingSlotViewSet(viewsets.ModelViewSet):
    queryset = ParkingSlot.objects.all()
    serializer_class = ParkingSlotSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['=date']

    def get_queryset(self):
        queryset = ParkingSlot.objects.all()
        date = self.request.query_params.get('date', None)
        time_slot = self.request.query_params.get('time_slot', None)
        if date is not None:
            if time_slot is not None:
                queryset = queryset.filter(date=date, time_slot=time_slot, is_available=True)
            else:
                queryset = queryset.filter(date=date, is_available=True)
        return queryset


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def create(self, request, *args, **kwargs):
        parking_slot_id = request.data.get('slot_number')
        customer_name = request.data.get('customer_name')
        customer_contact = request.data.get('contact_number')
        booking_date = request.data.get('date')

        # check if a booking already exists for the given customer contact
        if Booking.objects.filter(customer__contact_number=customer_contact).exists():
            return Response({"error": "A booking already exists for this customer contact."},
                            status=status.HTTP_400_BAD_REQUEST)

        # create or retrieve the customer object
        customer, created = Customer.objects.get_or_create(contact_number=customer_contact,
                                                           defaults={'name': customer_name})

        # retrieve the parking slot object
        try:
            parking_slot = ParkingSlot.objects.get(id=parking_slot_id, date=booking_date, is_available=True)
        except ParkingSlot.DoesNotExist:
            return Response({"error": "The selected parking slot is not available for booking."},
                            status=status.HTTP_400_BAD_REQUEST)

        # create the booking object and update the parking slot availability
        booking = Booking.objects.create(parking_slot=parking_slot, customer=customer)
        parking_slot.is_available = False
        parking_slot.save()

        serializer = self.get_serializer(booking)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='daily-report')
    def daily_report(self, request):
        date = request.query_params.get('date')
        if not date:
            return Response({'error': 'Please provide a date in format YYYY-MM-DD.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            bookings = Booking.objects.filter(date=date).annotate(total_duration=Sum('duration'))
            total_revenue = bookings.aggregate(Sum('amount'))['amount__sum']
            total_bookings = bookings.count()
            report_data = {
                'date': date,
                'total_bookings': total_bookings,
                'total_duration': bookings.aggregate(Sum('total_duration'))['total_duration__sum'],
                'total_revenue': total_revenue if total_revenue else 0,
            }
            return Response(report_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
# {
#     "customer_name": "John Doe",
#     "contact_number": "1234567890",
#     "date": "2023-04-27",
#     "slot_number": 3
# }
