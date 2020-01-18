from django.db import models
from products.models import Product

# Create your models here.

class List(models.Model):
    lista_id = models.CharField(max_length=100)
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




