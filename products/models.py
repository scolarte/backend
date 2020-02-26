from django.db import models
from decimal import *
from .size_and_quantities import TAMANIOS, CANTIDADES

class Category(models.Model):
    system_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories_images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return '{}'.format(self.name)




class Brand(models.Model):    
    #category = models.ForeignKey(Category, on_delete=models.CASCADE)
    system_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='subcategories_images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Brand: {}'.format(self.name)




class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)    
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    system_id = models.CharField(max_length=100, unique=True)
    large_name = models.CharField(max_length=250, unique=True)
    short_name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=250, unique=True)
    sku = models.CharField(max_length=20, unique=True, blank=True, null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(default=1.00, max_digits=6, decimal_places=2, null=True, blank=True)
    stock = models.IntegerField(default=100, null=True, blank=True)    
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('short_name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return '{}'.format(self.short_name)

class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:        
        verbose_name = 'Foto de Producto'
        verbose_name_plural = 'Fotos de Productos'
        
    def __str__(self):
        return '{}'.format(self.image)





class ProductItem(models.Model):
    lista = models.ForeignKey('lists.List', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100, blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
   
    def sub_total(self):
        return Decimal(self.product.price)

 


        
                