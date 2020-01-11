from django.urls import include, path

from .views import SignUpView, SellerSignUpView, ClientSignUpView


app_name = 'roles'

urlpatterns = [
    path('registro/', SignUpView.as_view(), name='signup'),
    path('registro/clientes', ClientSignUpView.as_view(), name='client_signup'),
    path('registro/vendedores', SellerSignUpView.as_view(), name='seller_signup'),
]