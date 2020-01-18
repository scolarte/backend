from django.db import models
from products.models import Product
from roles.models import User

# Create your models here.

class List(models.Model):
    LISTA_STATUS = (
        ('recibida_pagada', 'Recibida y pagada'),
        ('recibida_no_pagada', 'Recibida pero no pagada'),
        ('en_revision', 'En revision'),
        ('en_camino', 'En camino'),
        ('entregada', 'Entregada'),
        ('cancelada', 'Cancelada')
    )
    lista_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=LISTA_STATUS, default='recibida_pagada')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return str(self.id)


class ListItem(models.Model):
    lista = models.ForeignKey(List, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comment = models.CharField(max_length=100, blank=True, null=True, default='')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    step_two_complete = models.BooleanField(default=False)

    def sub_total(self):
        return int(self.product.price)




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