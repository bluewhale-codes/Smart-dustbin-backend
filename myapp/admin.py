from django.contrib import admin
from .models import MyUser,ClientProfile,VolunteerProfile,PickupBooking
# Register your models here.

admin.site.register(MyUser)
admin.site.register(ClientProfile)
admin.site.register(VolunteerProfile)
admin.site.register(PickupBooking)
