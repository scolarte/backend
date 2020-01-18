from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth.views import LogoutView, LoginView


from . import views

app_name = "core"

urlpatterns = [
    path('', views.ScolarteHome.as_view(), name='home'),
    path('<slug:c_slug>/productos/', views.all_prod_by_category, name='products_by_category'),
    path('categorias/', views.AllCategories.as_view(), name='categories'),
    path("salir/", LogoutView.as_view(), name="logout"),
    path("ingresar/", LoginView.as_view(template_name='scolarte/registration/login.html'), name="login"),
]