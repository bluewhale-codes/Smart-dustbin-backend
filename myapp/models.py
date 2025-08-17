from django.contrib.auth.models import User
from django.db import models
import uuid
from django.core.validators import RegexValidator
from cloudinary.models import CloudinaryField
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
    profile_image = CloudinaryField("image", blank=True, null=True)
    address = models.TextField(blank=True)
    contact_no = models.CharField(
        null=True,
        blank=True,
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?\d{10,15}$', message="Enter a valid phone number (10-15 digits).")],
        help_text="Include country code. Example: +919876543210"
    )
    


    def __str__(self):
        return f"Client Profile - {self.myuser.full_name}"

    
class PickupBooking(models.Model):
    STATUS_CHOICES = (
        ("unassigned", "Unassigned"),   # Task is not assigned to anyone yet
        ("active", "Active"),           # Task is accepted and in progress
        ("completed", "Completed"),     # Task is done
    )
    booking_id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        unique=True
    )

    my_user = models.ForeignKey(
        MyUser,
        on_delete=models.CASCADE,
        related_name="bookings"
    )
    

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="unassigned",
    )
    
    

    # Latitude & Longitude for map-based location
    latitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True
    )
    longitude = models.DecimalField(
        max_digits=9, 
        decimal_places=6, 
        null=True, 
        blank=True
    )

    time_slot = models.DateTimeField()
    waste_type = models.CharField(max_length=100)
    approximate_weight = models.DecimalField(max_digits=6, decimal_places=2)

    # Existing instructions
    special_instructions = models.TextField(blank=True, null=True)
    garbage_image = CloudinaryField("image", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        # Safe fallback if full_name is missing
        name = getattr(self.my_user, 'full_name', str(self.my_user))
        return f"Booking {self.booking_id} by {name}  on {self.time_slot}"

# Volunteer-specific details
class VolunteerProfile(models.Model):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )
    
    volunteer_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    myuser = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name="volunteer_profile")
    date_of_birth = models.DateField(null=True,blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES,blank=True,null=True)

    # New optional one-to-one field
    task = models.OneToOneField(
        PickupBooking,
        on_delete=models.SET_NULL,   # If booking is deleted, this field becomes null
        null=True,
        blank=True,
        related_name="mytask"
    )
    id_number = models.CharField(max_length=20, unique=True,blank=True,null=True, help_text="Aadhaar or PAN number")
    id_proof =CloudinaryField("image", blank=True, null=True)
    profile_image =CloudinaryField("image", blank=True, null=True)
    address = models.TextField(blank=True)
    contact_no = models.CharField(
        null=True,
        blank=True,
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?\d{10,15}$', message="Enter a valid phone number (10-15 digits).")],
        help_text="Include country code. Example: +919876543210"
    )

    def __str__(self):
        return f"Volunteer Profile - {self.myuser.full_name}"
