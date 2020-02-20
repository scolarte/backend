from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse_lazy

from core import views

app_name = "core"

urlpatterns = [
    path('', views.ScolarteHome, name='home'),
    path("salir/", LogoutView.as_view(), name="logout"),
    path("ingresar-cliente-vendedor/", views.ScolarteLogin.as_view(template_name='scolarte/registration/login_client_seller.html'), name="login_client_seller"),
    path("ingresar/", views.MyLoginView.as_view(template_name='scolarte/registration/login.html', success_url=reverse_lazy('core:home')), name="login"),
]