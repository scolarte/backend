from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.urls import reverse, reverse_lazy
from decouple import config

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
    path('cambiar-password', auth_views.PasswordChangeView.as_view(
        template_name="scolarte/registration/change_password.html",
        success_url = "/cuentas/cambiar-password/exitoso"
    ), name = "change_password"),
    path('cambiar-password/exitoso', auth_views.PasswordChangeView.as_view(
        template_name="scolarte/registration/change_password_success.html"        
    ), name = "change_password_success"),
    # Path for recovery passwords
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='scolarte/registration/password_reset.html',
             subject_template_name='scolarte/registration/password_reset_subject.txt',
             from_email=config('FROM_EMAIL'),
             email_template_name='scolarte/registration/password_reset_email.html',
             success_url= reverse_lazy('roles:password_reset_done')
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='scolarte/registration/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='scolarte/registration/password_reset_confirm.html',
             success_url= reverse_lazy('roles:password_reset_complete')
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='scolarte/registration/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]