from django.contrib import admin
from .models import Storehouse, Box, UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Storehouse)
class StorehouseAdmin(admin.ModelAdmin):
    pass

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    pass


# Register your models here.
