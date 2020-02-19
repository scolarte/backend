from django.urls import include, path

from .views import (
    SignUpView, SellerSignUpView,
    ClientSignUpView, MyClientSignupView, update_client_profile
)


app_name = 'roles'

#preppend cuentas/

urlpatterns = [
    #path('registro/', SignUpView.as_view(), name='signup'),
    path('registro/clientes', MyClientSignupView, name='client_signup'),
    path('perfil/', update_client_profile, name='profile_update'),
]