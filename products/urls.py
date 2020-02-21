from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth.views import LogoutView, LoginView


from . import views

app_name = "products"

urlpatterns = [
    path('', views.ProductsListView.as_view(), name='all_products'),
    path('categorias/', views.AllCategories.as_view(), name='categories'),
    path('marcas-csv/', views.brands_upload, name="brands_upload"),
    path('productos-csv/', views.products_upload, name="products_upload"),    
    path('categorias-csv/', views.categories_upload, name="categories_upload"),
]