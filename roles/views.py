from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from roles.models import *
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Count
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from .forms import SellerSignUpForm, ClientSignUpForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from decouple import config

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
        print("## Usuario se registro!!!")
        try:
            print("Se envió email de Signup Confirmation")
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            # html_content = get_template('scolarte/registration/signup_confirmation.html').render({'revenue': '120'})   
            #content = Content("text/html", html_content)
            #print(form.user.email)
            message = Mail(
                        from_email=config('FROM_EMAIL'),
                        to_emails='oma.gonzales@gmail.com',
                        subject="on user signup is working",
                        template_id= "186cd80a909d439f8c92b1830120180a",
                        dynamic_template_data={'username': user.username})
            sg.send(message)
        except:
            print("No se pudo enviar email de confirmación")    
            #print("Form mail: ", form.user.email)
            print("Settings FROM EMAIL: ", config('FROM_EMAIL'))
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
        form = ClientSignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            
            html_content = '<strong>Gracias por registarte </strong>' + username            

            message = Mail(
                        from_email=config('FROM_EMAIL'),
                        to_emails=form.instance.email,
                        subject='Escolarte: ¡Bienvenido ' + username + '!',
                        html_content=html_content)
            message.dynamic_template_data = {
                'username': username
                }
            message.template_id = 'd-186cd80a909d439f8c92b1830120180a'
            try:
                sg = SendGridAPIClient(config('SENDGRID_API_KEY'))                
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(str(e))
            login(request, user)    
            return redirect('core:home')
        else:
            raise Http404("Registro no exitoso.")
    else:

        client_form = ClientSignUpForm()

        return render(request, 'scolarte/registration/signup_form.html', {
            'client_form': client_form,            
            'user_type': 'cliente'
        })





@login_required
@csrf_exempt
def update_client_profile(request):
    user = request.user
    
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES,
                                       instance=user.profile) 
        if profile_form.is_valid():
            profile_form.save(commit=True)
            return redirect('core:home')
        else:
            return HttpResponse("No se grabó el perfil")
            
    else:
        profile_form = ProfileForm(instance=user.profile)
        return render(request, 'scolarte/profile/perfil.html', {'client_profile_form': profile_form})



### Seller SignUp


# @transaction.atomic
# def MySellerSignupView(request):

#     provincias_list = ["Azuay", "Bolívar", "Cañar", "Carchi", "Chimborazo"]
#     cantones_list = ["Aguarico", "Baba", "Daule", "Echeandía", "Flavio Alfaro"]
#     parroquias_list = ["Parroquia1", "Parroquia2", "Parroqui3", "Parroquia4", "Parroquia5"]

    
#     if request.method == 'POST':

       
#         seller_form = SellerSignUpForm(request.POST)
#         seller_profile_form = ProfileForm(provincias_list, cantones_list, parroquias_list, request.POST, request.FILES)

#         if seller_form.is_valid() and seller_profile_form.is_valid():
#             seller = seller_form.save()
#             #client.is_active = True
#             #client.save()
#             username = seller_form.cleaned_data.get('username')
#             signup_user = User.objects.get(username=username)
#             customer_group = Group.objects.get(name='Vendedores')
#             customer_group.user_set.add(signup_user)
#             raw_password = seller_form.cleaned_data.get('password1')
#             seller.refresh_from_db()  # This will load the Profile created by the Signal

#             seller_profile_form = ProfileForm(provincias_list, cantones_list, parroquias_list, request.POST, request.FILES,
#                                        instance=seller.profile)  # Reload the profile form with the profile instance
#             seller_profile_form.full_clean()  # Manually clean the form this time. It is implicitly called by "is_valid()" method
#             seller_profile_form.save()  # Gracefully save the form
#             #send_email_new_registered_user(user.id) # send email to admin when a new user registers himself
#             login(request, seller)
#             return redirect('core:home')

#         else:
#             pass


#     else:

#         seller_form = SellerSignUpForm()

#         seller_profile_form = ProfileForm(provincias_list, cantones_list, parroquias_list)

#         return render(request, 'scolarte/registration/signup_form.html', {
#             'seller_form': seller_form,
#             'seller_profile_form': seller_profile_form,
#             'user_type': 'vendedor'
#         })

