from django.contrib.auth.models import User
from django.db import models
import uuid

# Common profile for both volunteer & client
class MyUser(models.Model):
    USER_TYPE_CHOICES = (
        ("client", "Client"),
        ("volunteer", "Volunteer"),
    )
    
    myuser_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="myuser")
    full_name = models.CharField(max_length=100, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    

    def __str__(self):
        return f"{self.full_name} - {self.user_type}"


# Client-specific details
class ClientProfile(models.Model):
    client_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    myuser = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name="client_profile")
    address = models.TextField(blank=True)
    landmark = models.CharField(max_length=255, blank=True)
    

    def __str__(self):
        return f"Client Profile - {self.myuser.full_name}"


# Volunteer-specific details
class VolunteerProfile(models.Model):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )
    
    volunteer_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    myuser = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name="volunteer_profile")
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    # id_proof = models.FileField(upload_to="volunteer_id_proofs/")
    # profile_image = models.ImageField(upload_to="volunteer_profiles/")

    def __str__(self):
        return f"Volunteer Profile - {self.myuser.full_name}"