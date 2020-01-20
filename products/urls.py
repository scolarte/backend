from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth.views import LogoutView, LoginView


from . import views

app_name = "products"

urlpatterns = [
    path('', views.ProductsListView.as_view(), name='all_products'),
    path('<slug:c_slug>/productos/', views.all_prod_by_category, name='products_by_category'),
    path('categorias/', views.AllCategories.as_view(), name='categories'),
]