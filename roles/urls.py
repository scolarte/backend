from django.urls import include, path

from .views import (
    SignUpView, SellerSignUpView,
    ClientSignUpView, MyClientSignupView,
    MySellerSignupView
)


app_name = 'roles'

urlpatterns = [
    path('registro/', SignUpView.as_view(), name='signup'),
    path('registro/clientes', MyClientSignupView, name='client_signup'),
    path('registro/vendedores', MySellerSignupView, name='seller_signup'),
]