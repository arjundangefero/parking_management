from rest_framework.routers import DefaultRouter
from .views import ParkingSlotViewSet , BookingViewSet
from django.urls import path
from .views import MyObtainTokenPairView
from rest_framework_simplejwt.views import TokenRefreshView


router = DefaultRouter()
router.register(r'parking-slots', ParkingSlotViewSet)
router.register(r'bookings', BookingViewSet)

urlpatterns = [
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


urlpatterns += router.urls
