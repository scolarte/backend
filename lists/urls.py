from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth.views import LogoutView, LoginView


from . import views

app_name = "lists"

urlpatterns = [
    path('', views.ListFormView.as_view(), name='my_lists'),
    path('agregar-producto/', views.add_product_to_list, name='add_product_to_list'),
    path('mis-listas/', views.update_lists_count, name='update_lists_count'),
    path('lista-detalles/<int:lista_id>/', views.ListDetailsFormView.as_view(), name='list_details'),
    path('escuelas-csv/', views.schools_upload, name="schools_upload"),
    path('borrar-producto-de-lista/<int:listitem_id>/', views.full_remove_listitem, name='full_remove_listitem'),
    path('borrar-lista/<int:lista_id>/', views.full_remove_list, name='full_remove_list'),
    path('borrar-escuela/<int:school_id>/', views.full_remove_school, name='full_remove_school'),
]

