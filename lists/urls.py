from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth.views import LogoutView, LoginView


from . import views

app_name = "lists"

urlpatterns = [
    path('agregar-producto/', views.add_product_to_list, name='add_product_to_list'),
    path('mis-listas/', views.AllLists.as_view(), name='my_lists'),
]