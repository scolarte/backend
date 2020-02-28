from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import List, School, ListItem



# Register your models here.

class ListItemAdminInline(admin.TabularInline):    
    model = ListItem    
    exclude = ['step_two_complete']
    extra = 3
class ListAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    inlines = [ ListItemAdminInline, ]
    list_display = ['id','name', 'status', 'list_image', 'user', 'seller', 'status', 'modified_at']   
    list_filter = ('status', 'modified_at', 'created_at')
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'seller__username']
    list_display_links = ('id', 'name', 'list_image', )

admin.site.register(List, ListAdmin)

# class ListItemAdmin(admin.ModelAdmin):
#     list_display = ['id']   

# admin.site.register(ListItem, ListItemAdmin)



class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at'] 
    search_fields = ['name', ]
    list_filter = ('created_at', )

admin.site.register(School, SchoolAdmin)