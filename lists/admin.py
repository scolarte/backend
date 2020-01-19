from django.contrib import admin
from .models import List, School, ListItem



# Register your models here.


class ListAdmin(admin.ModelAdmin):
    list_display = ['name', 'status']   

admin.site.register(List, ListAdmin)



class ListItemAdmin(admin.ModelAdmin):
    list_display = ['id']   

admin.site.register(ListItem, ListItemAdmin)



class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'provincia']   

admin.site.register(School, SchoolAdmin)