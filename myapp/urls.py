from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RegisterView , MeView 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
     path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
     path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Current user profile (JWT required)
    path("me/", MeView.as_view(), name="me"),
]