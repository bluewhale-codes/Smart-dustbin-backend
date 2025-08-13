from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework.views import APIView
from .models import MyUser, ClientProfile, VolunteerProfile
from .serializers import MyuserProfileSerializer, ClientProfileSerializer, VolunteerProfileSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        myuser = serializer.save()

        # Get the related profile data
        if myuser.user_type == "client":
            profile_data = ClientProfileSerializer(myuser.client_profile).data
        else:
            profile_data = VolunteerProfileSerializer(myuser.volunteer_profile).data

        return Response(
            {
                "message": "Registered successfully",
                "user_type": myuser.user_type,
                
                "profile": profile_data,
            },
            status=201,
        )
    

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        myuser_data = MyuserProfileSerializer(request.user.myuser).data

        # Decide which profile serializer to use
        if request.user.myuser.user_type == "client":
            profile_data = ClientProfileSerializer(request.user.myuser.client_profile).data
        elif request.user.myuser.user_type == "volunteer":
            profile_data = VolunteerProfileSerializer(request.user.myuser.volunteer_profile).data
        else:
            profile_data = {}

        return Response({
            "myuser": myuser_data,
            "profile": profile_data
        })
