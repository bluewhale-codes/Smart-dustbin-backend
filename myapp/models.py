from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
import uuid

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Phone number is required")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ("client", "Client"),       # Wants garbage collection
        ("volunteer", "Volunteer"), # Collects garbage
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=100, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.full_name} ({self.phone})"

# Create your models here.
class ClientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="client_profile")
    address = models.TextField()
    landmark = models.CharField(max_length=255, blank=True)
    preferred_pickup_time = models.TimeField(blank=True, null=True)

    def __str__(self):
        return f"Client Profile - {self.user.full_name}"

class VolunteerProfile(models.Model):
    GENDER_CHOICES = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="volunteer_profile")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField()
    id_proof = models.FileField(upload_to="volunteer_id_proofs/")
    profile_image = models.ImageField(upload_to="volunteer_profiles/")

    def __str__(self):
        return f"Volunteer Profile - {self.user.full_name}"
