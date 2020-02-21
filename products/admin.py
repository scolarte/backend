from django.contrib import admin
from .models import Category, SubCategory, Brand, Product, ProductPhoto

# Register your models here.
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}
    list_filter = ('created_at', 'modified_at')  

admin.site.register(Brand, BrandAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}    

admin.site.register(Category, CategoryAdmin)


# Register your models here.
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ['category', 'system_id', 'name', 'slug']
    prepopulated_fields = {'slug':('name',)}
    list_per_page = 20

admin.site.register(SubCategory, SubCategoryAdmin)

# Register your models here.

class ProductImageInline(admin.StackedInline):
    model = ProductPhoto    
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ ProductImageInline, ]
    model = Product
    list_display = ['short_name', 'price', 'stock', 'available', 'created_at', 'modified_at']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug':('short_name',)}
    list_per_page = 20
    