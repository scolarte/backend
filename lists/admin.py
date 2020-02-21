from django.contrib import admin
from .models import List, School, ListItem



# Register your models here.


class ListAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'status', 'user', 'seller', 'status', 'created_at', 'modified_at']   
    list_filter = ('status', 'modified_at', 'created_at')
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'seller__username']

admin.site.register(List, ListAdmin)



class ListItemAdmin(admin.ModelAdmin):
    list_display = ['id']   

admin.site.register(ListItem, ListItemAdmin)



class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at'] 
    search_fields = ['name', ]
    list_filter = ('created_at', )

admin.site.register(School, SchoolAdmin)