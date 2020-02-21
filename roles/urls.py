from django.urls import include, path
from django.contrib.auth import views as auth_views

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
    path('password-reset', auth_views.PasswordResetView.as_view(template_name="scolarte/registration/password_reset.html"), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(template_name="scolarte/registration/password_reset_confirm.html"), name='password_reset_confirm'),
    path('password_reset_complete/$',auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]