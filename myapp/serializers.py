from rest_framework import serializers
from django.contrib.auth.models import User
from .models import MyUser, ClientProfile, VolunteerProfile


class RegisterSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=15)
    username = serializers.CharField(max_length=15)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=6)
    user_type = serializers.ChoiceField(choices=MyUser.USER_TYPE_CHOICES)
    address = serializers.CharField(required=False, allow_blank=True)
    landmark = serializers.CharField(required=False, allow_blank=True)
    date_of_birth = serializers.DateField(required=False)  # For volunteer
    gender = serializers.ChoiceField(choices=VolunteerProfile.GENDER_CHOICES, required=False)

    def validate(self, attrs):
        # Phone number used as username
        if User.objects.filter(username=attrs["username"]).exists():
            raise serializers.ValidationError({"phone": "username already registered"})
        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError({"email": "Email already registered"})
        
        # Volunteer-specific validation
        if attrs["user_type"] == "volunteer":
            if not attrs.get("date_of_birth") or not attrs.get("gender"):
                raise serializers.ValidationError({"volunteer": "Date of birth and gender are required for volunteers"})
        
        return attrs

    def create(self, validated):
        # 1. Create Django User
        user = User.objects.create_user(
            username=validated["username"],
            email=validated["email"],
            password=validated["password"],
            first_name=validated["full_name"],
        )

        # 2. Create MyUser
        myuser = MyUser.objects.create(
            user=user,
            full_name=validated["full_name"],
            user_type=validated["user_type"],
        )

        # 3. Create related profile based on user type
        if validated["user_type"] == "client":
           ClientProfile.objects.create(
                myuser=myuser,
                address=validated.get("address", ""),
                landmark=validated.get("landmark", ""),
            )
        elif validated["user_type"] == "volunteer":
            VolunteerProfile.objects.create(
                myuser=myuser,
                date_of_birth=validated["date_of_birth"],
                gender=validated["gender"],
            )

        return  myuser
    
class MyuserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ["myuser_id", "full_name", "user_type"]
class ClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = ["client_id", "address", "landmark"]

class VolunteerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = VolunteerProfile
        fields = ["volunteer_id", "date_of_birth", "gender"]