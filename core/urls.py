from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth.views import LogoutView, LoginView


from . import views

app_name = "core"

urlpatterns = [
    path('', views.ScolarteHome.as_view(), name='home'),
    path("salir/", LogoutView.as_view(), name="logout"),
    path("ingresar/", LoginView.as_view(template_name='scolarte/registration/login.html'), name="login"),
    
]