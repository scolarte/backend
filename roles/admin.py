from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import User, Profile
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password

# class UserResource(resources.ModelResource):
#     class Meta:
#         model: User
class UserAdmin(ImportExportModelAdmin, BaseUserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_client', 'is_seller', 'is_active', 'date_joined')
    list_filter = ('date_joined', 'is_client', 'is_seller')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Informacion Personal', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'groups', 'user_permissions')}),
        ('Tipo de Usuaro', {'fields': ('is_client', 'is_seller')}),        
    )    
    

admin.site.register(User, UserAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'cedula_ruc', 'birthdate', 'created'] 
    search_fields = ['user__username', 'user__email', 'user__first_name', 'user__last_name', 'cedula_ruc' ]
    list_filter = ('created',  )

admin.site.register(Profile, ProfileAdmin)

