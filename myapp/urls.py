from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClientProfileUpdateView, UpdatePickupBookingStatus, RegisterView , MeView ,PickupBookingViewSet , PublicPickupBookingViewSet,VolunteerProfileUpdateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'bookings', PickupBookingViewSet, basename="pickupbooking")
router.register(r'public-bookings', PublicPickupBookingViewSet, basename="public-bookings")

urlpatterns = [
     path("register/", RegisterView.as_view(), name="register"),
     path("api/bookings/<uuid:booking_id>/status/", UpdatePickupBookingStatus.as_view(), name="update-booking-status"),
     path('api/', include(router.urls)),
     path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
     path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Current user profile (JWT required)
    path("me/", MeView.as_view(), name="me"),
    path('volunteer-profiles/me/update/', VolunteerProfileUpdateView.as_view(), name='volunteer-create'),
    path('client-profiles/me/update/', ClientProfileUpdateView.as_view(), name='client-update-me'),
]