from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_client', 'is_seller', 'is_active', 'date_joined')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informacion Personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Tipo de Usuaro', {'fields': ('is_client', 'is_seller')}),        
    )
admin.site.register(User, UserAdmin)
admin.site.register(Profile)

