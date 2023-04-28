from rest_framework.routers import DefaultRouter
from .views import ParkingSlotViewSet , BookingViewSet

router = DefaultRouter()
router.register(r'parking-slots', ParkingSlotViewSet)
router.register(r'bookings', BookingViewSet)
urlpatterns = [
    # Your other URL patterns here
]

urlpatterns += router.urls
