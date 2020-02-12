from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

UserAdmin.list_display = ('username', 'first_name', 'last_name', 'email', 'is_client', 'is_seller', 'is_active', 'date_joined')
UserAdmin.list_filter = ('is_client', 'is_seller', 'is_staff') 
admin.site.register(User, UserAdmin)

admin.site.register(Profile)

