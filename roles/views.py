from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from roles.models import *
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from .forms import SellerSignUpForm, ClientSignUpForm, ProfileForm


# Create your views here.
def home(request):
    return HttpResponse("Hola")


class SignUpView(TemplateView):
    template_name = 'scolarte/registration/signup.html'


####


class ClientSignUpView(CreateView):
    model = User
    form_class = ClientSignUpForm
    template_name = 'scolarte/registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'cliente'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('core:home')


class SellerSignUpView(CreateView):
    model = User
    form_class = SellerSignUpForm
    template_name = 'scolarte/registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'vendedor'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('core:home')



### SignupView 2 forms


@transaction.atomic
def MyClientSignupView(request):

    provincias_list = ["Azuay", "Bolívar", "Cañar", "Carchi", "Chimborazo"]
    cantones_list = ["Aguarico", "Baba", "Daule", "Echeandía", "Flavio Alfaro"]
    parroquias_list = ["Parroquia1", "Parroquia2", "Parroqui3", "Parroquia4", "Parroquia5"]

    
    if request.method == 'POST':

       
        client_form = ClientSignUpForm(request.POST)
        client_profile_form = ProfileForm(provincias_list, cantones_list, parroquias_list, request.POST, request.FILES)

        if client_form.is_valid() and client_profile_form.is_valid():
            client = client_form.save()
            #client.is_active = True
            #client.save()
            username = client_form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            customer_group = Group.objects.get(name='Clientes')
            customer_group.user_set.add(signup_user)
            raw_password = client_form.cleaned_data.get('password1')
            client.refresh_from_db()  # This will load the Profile created by the Signal

            client_profile_form = ProfileForm(provincias_list, cantones_list, parroquias_list, request.POST, request.FILES,
                                       instance=client.profile)  # Reload the profile form with the profile instance
            client_profile_form.full_clean()  # Manually clean the form this time. It is implicitly called by "is_valid()" method
            client_profile_form.save()  # Gracefully save the form
            #send_email_new_registered_user(user.id) # send email to admin when a new user registers himself
            login(request, client)
            return redirect('core:home')

        else:
            pass


    else:

        client_form = ClientSignUpForm()

        client_profile_form = ProfileForm(provincias_list, cantones_list, parroquias_list)

        return render(request, 'scolarte/registration/signup_form.html', {
            'client_form': client_form,
            'client_profile_form': client_profile_form,
            'user_type': 'cliente'
        })



### Seller SignUp


@transaction.atomic
def MySellerSignupView(request):

    provincias_list = ["Azuay", "Bolívar", "Cañar", "Carchi", "Chimborazo"]
    cantones_list = ["Aguarico", "Baba", "Daule", "Echeandía", "Flavio Alfaro"]
    parroquias_list = ["Parroquia1", "Parroquia2", "Parroqui3", "Parroquia4", "Parroquia5"]

    
    if request.method == 'POST':

       
        seller_form = SellerSignUpForm(request.POST)
        seller_profile_form = ProfileForm(provincias_list, cantones_list, parroquias_list, request.POST, request.FILES)

        if seller_form.is_valid() and seller_profile_form.is_valid():
            seller = seller_form.save()
            #client.is_active = True
            #client.save()
            username = seller_form.cleaned_data.get('username')
            signup_user = User.objects.get(username=username)
            customer_group = Group.objects.get(name='Vendedores')
            customer_group.user_set.add(signup_user)
            raw_password = seller_form.cleaned_data.get('password1')
            seller.refresh_from_db()  # This will load the Profile created by the Signal

            seller_profile_form = ProfileForm(provincias_list, cantones_list, parroquias_list, request.POST, request.FILES,
                                       instance=seller.profile)  # Reload the profile form with the profile instance
            seller_profile_form.full_clean()  # Manually clean the form this time. It is implicitly called by "is_valid()" method
            seller_profile_form.save()  # Gracefully save the form
            #send_email_new_registered_user(user.id) # send email to admin when a new user registers himself
            login(request, seller)
            return redirect('core:home')

        else:
            pass


    else:

        seller_form = SellerSignUpForm()

        seller_profile_form = ProfileForm(provincias_list, cantones_list, parroquias_list)

        return render(request, 'scolarte/registration/signup_form.html', {
            'seller_form': seller_form,
            'seller_profile_form': seller_profile_form,
            'user_type': 'vendedor'
        })

