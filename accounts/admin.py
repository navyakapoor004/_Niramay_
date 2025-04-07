from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import customuser

# Register the custom user model with the admin panel
class CustomUserAdmin(UserAdmin):
    model = customuser
    # Specify the fields you want to display in the admin panel
    list_display = ['username', 'email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['username', 'email']
    ordering = ['username']

admin.site.register(customuser, CustomUserAdmin)