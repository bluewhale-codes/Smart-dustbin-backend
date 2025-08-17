from rest_framework import generics, permissions ,viewsets,status
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from .models import PickupBooking , VolunteerProfile , ClientProfile

from .serializers import UserProfileSerializer, PickupBookingStatusUpdateSerializer, MyuserProfileSerializer, ClientProfileSerializer, VolunteerProfileSerializer,PickupBookingSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        myuser = serializer.save()
        profile_data = MyuserProfileSerializer(myuser).data
        # # Get the related profile data
        # if myuser.user_type == "client":
        #     profile_data = ClientProfileSerializer(myuser.client_profile).data
        # else:
        #     profile_data = VolunteerProfileSerializer(myuser.volunteer_profile).data

        return Response(
            {
                "message": "Registered successfully",
                "profile": profile_data,
            },
            status=201,
        )
    

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    task_data = None

    def get(self, request):
        myuser_data = MyuserProfileSerializer(request.user.myuser).data
        user_data = UserProfileSerializer(request.user).data
        
        # Decide which profile serializer to use
        if request.user.myuser.user_type == "client":
            profile_data = ClientProfileSerializer(request.user.myuser.client_profile).data
        elif request.user.myuser.user_type == "volunteer":
             profile_data = VolunteerProfileSerializer(request.user.myuser.volunteer_profile).data
             # Fetch task (PickupBooking) if exists
             volunteer_profile = request.user.myuser.volunteer_profile
             if hasattr(volunteer_profile, 'task') and volunteer_profile.task is not None:
                 task_data = PickupBookingSerializer(volunteer_profile.task).data
        else:
             profile_data = {}
        
        return Response({
            "myuser": myuser_data,
            "user" : user_data,
            "profile":profile_data
        })
    
class PickupBookingViewSet(viewsets.ModelViewSet):
    serializer_class = PickupBookingSerializer
    permission_classes = [permissions.IsAuthenticated]  # JWT required

    def get_queryset(self):
        # ✅ Only return bookings of the logged-in user
        return PickupBooking.objects.filter(my_user=self.request.user.myuser).order_by('-created_at')

    def perform_create(self, serializer):
        # ✅ Auto-assign the logged-in user
        serializer.save(my_user=self.request.user.myuser)

class PublicPickupBookingViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Public API: anyone can see all bookings (no authentication required)
    """
    queryset = PickupBooking.objects.all()
    serializer_class = PickupBookingSerializer
    permission_classes = [permissions.AllowAny]  # ✅ no auth required

class UpdatePickupBookingStatus(APIView):
    permission_classes = [permissions.IsAuthenticated]  # Only logged-in users can update

    def patch(self, request, booking_id):
        try:
            booking = PickupBooking.objects.get(booking_id=booking_id)
        except PickupBooking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PickupBookingStatusUpdateSerializer(booking, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class VolunteerProfileUpdateView(generics.RetrieveUpdateAPIView):
    
    serializer_class = VolunteerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def get_object(self):
        return self.request.user.myuser.volunteer_profile

class ClientProfileUpdateView(generics.RetrieveUpdateAPIView):
    
    serializer_class = ClientProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def get_object(self):
        return self.request.user.myuser.client_profile

