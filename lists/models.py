from django.db import models
from products.models import Product
from roles.models import User
import uuid

# Create your models here.

class School(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=False)
    address_reference = models.CharField(max_length=100, blank=False)
    provincia = models.CharField(max_length=100, blank=False, null=True)
    canton = models.CharField(max_length=100, blank=False, null=True)
    parroquia = models.CharField(max_length=100, blank=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return str(self.name)




class List(models.Model):
    LISTA_STATUS = (
        ('Recibida y pagada', 'Recibida y pagada'),
        ('Recibida pero no pagada', 'Recibida pero no pagada'),
        ('En revision', 'En revision'),
        ('Lista pedida', 'Lista pedida'),
        ('En camino', 'En camino'),
        ('Entregada', 'Entregada'),
        ('Cancelada', 'Cancelada')
    )
    name = models.CharField(max_length=100, default='Lista anónima')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seller = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='vendedor')
    school = models.ForeignKey(School, on_delete=models.CASCADE,  null=True, blank=True)
    status = models.CharField(max_length=40, choices=LISTA_STATUS, default='Recibida pero no pagada')
    seller_status = models.CharField(max_length=40, choices=LISTA_STATUS, default='En revision')
    list_image = models.FileField(upload_to='lists_images', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']   

    def __str__(self):
        return str(self.id)


class ListItem(models.Model):
    lista = models.ForeignKey(List, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1, blank=True, null=True)
    comment = models.CharField(max_length=100, blank=True, null=True, default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    step_two_complete = models.BooleanField(default=False)

    def sub_total(self):
        return int(self.product.price * self.quantity)


