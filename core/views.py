from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
from products.models import Category, Brand, Product
from django.contrib.auth.views import LoginView, SuccessURLAllowedHostsMixin
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from .forms import LoginForm
from django.shortcuts import render, redirect


# Create your views here.


def ScolarteHome(request):
    if request.user.is_authenticated:
        return redirect('products:all_products')
    else:
        return redirect('core:login')



class ScolarteLogin(TemplateView):
    template_name = "scolarte/login_cliente_seller.html"


class MyLoginView(LoginView):
    """
    Display the login form and handle the login action.
    """
    authentication_form = LoginForm
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        msg = {'cliente': 'Ingresar como cliente', 'vendedor': 'Ingresar como vendedor'}
        context['msg'] = msg.get(self.request.GET.get('cliente-o-vendedor'), '')
        return context