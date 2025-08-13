from django.contrib import admin
from .models import MyUser,ClientProfile,VolunteerProfile
# Register your models here.

admin.site.register(MyUser)
admin.site.register(ClientProfile)
admin.site.register(VolunteerProfile)
