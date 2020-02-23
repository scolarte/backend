from django.shortcuts import render, redirect
from .models import List, ListItem, School
from products.models import Product, ProductItem
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect
from .forms import ListForm, ListFormAllLists
from django.urls import reverse_lazy, reverse
from roles.models import User
import csv, io
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.shortcuts import get_list_or_404, get_object_or_404
import os
import json
from scolarte import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.http import JsonResponse


# Create your views here.
### List Details ###

def full_remove_list(request, lista_id):
    lista = List.objects.get(id=lista_id)
    lista.delete()
    return redirect(reverse('lists:my_lists'))


def full_remove_listitem(request, listitem_id):
    list_item = ListItem.objects.get(id=listitem_id)
    list_item.delete()
    lista_id = list_item.lista.id
    return redirect('lists:list_details', lista_id=lista_id)


def full_remove_school(request, school_id):
    school = School.objects.get(id=school_id)
    school.delete()
    return redirect('lists:schools_upload')   


def remove_list_assigned_to_seller(request, lista_id):
    lista = List.objects.get(id=lista_id)
    lista.seller = None
    lista.save()
    return redirect(reverse('lists:my_lists'))


# def order_list(request, lista_id):
#     lista = List.objects.get(id=lista_id)
#     lista.status = "Lista pedida"
#     lista.save()
#     return redirect(reverse('lists:my_lists'))  


@csrf_exempt
def order_list(request):

    lista_id = request.POST.get('lista_id')
    lista = List.objects.get(id=lista_id)
    lista.status = "Lista pedida"
    lista.save()

    return HttpResponse("post request success")
        
 



class ListDetailsFormView(LoginRequiredMixin, UpdateView):
    model = List
    form_class = ListForm
    context_object_name = 'lista'
    pk_url_kwarg  = 'lista_id'
    template_name = "scolarte/listas/lista-detalles.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        list_items = ListItem.objects.filter(lista=self.object)
        context['list_items'] = list_items
        context['list_items_count'] = len(list_items)
        list_total = 0
        for list_item in list_items:
            list_total += Decimal(list_item.sub_total())
        context['list_total'] = list_total
        return context

    def form_valid(self, form):
        if form.instance.status == 'entregada':
            html_content = '<strong>Hemos recibido la confirmación de tu orden: </strong>' + str(form.instance.id)
            message = Mail(
                from_email='sendgrid@example.com',
                to_emails=self.request.user.email,
                subject='Escolart: ¡Orden ' + str(form.instance.id) + ' confirmada!',
                html_content=html_content)
            try:
                sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print(str(e))
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('lists:list_details', kwargs={'lista_id': self.object.pk})



@csrf_exempt
def add_product_to_list(request):

    print("Enters Add Product to List")

    lista_id = request.POST.get('lista_id')
    if lista_id:
        try:
            lista = List.objects.get(id=lista_id)
        except:
            lista = List.objects.create(name="Lista anónima",
        user=request.user)
              
    else:
        total_listas = len(List.objects.all())
        if total_listas > 0:
            lista = List.objects.create(name="Lista anónima",
            user=request.user)
        else:
            lista = List.objects.create(name="Mi primera lista",
            user=request.user)


    
    product_id = request.POST.get('product_id')
    quantity = request.POST.get('quantity')

    try:

        product = Product.objects.get(id=product_id)

        list_item = ListItem.objects.create(
            lista=lista,
            product=product,
            quantity=quantity,
            comment="")
       
        return HttpResponse("post request success")
        

    except Exception as e:
        raise e



class ListGridView(LoginRequiredMixin, FormView):
    form_class = ListFormAllLists
    template_name = "scolarte/listas/lista_form.html"
    success_url = reverse_lazy('lists:my_lists')
    
    def form_valid(self, form):
        form = ListFormAllLists(self.request.POST, self.request.FILES)
        form = form.save(commit=False)
        form.user = self.request.user  # use your own profile here
        form.save()
        return HttpResponseRedirect(self.get_success_url())

class ListFormView(LoginRequiredMixin, TemplateView):    
    template_name = "scolarte/listas/listas.html"
    uccess_url = reverse_lazy('lists:my_lists')  

    def get(self, request, *args, **kwargs):
        if request.user.is_client:
            context = self.get_context_data(**kwargs)
            context['listas'] = List.objects.filter(user=request.user)
            return self.render_to_response(context)
        elif request.user.is_seller:
            context = self.get_context_data(**kwargs)
            seller = User.objects.get(id = request.user.id)
            context['listas'] = List.objects.filter(seller=seller)
            return self.render_to_response(context)
    

@csrf_exempt
def update_lists_count(request):
    if request.user.is_client:
        listas = List.objects.filter(user=request.user)
    elif request.user.is_seller:
        listas = List.objects.filter(seller=request.user)
    
    if not listas:
        mi_primera_lista = List.objects.create(name="Mi primera lista",
        user=request.user)
        return render(request, 'scolarte/listas/listas-de-usuario.html', {'mi_primera_lista':mi_primera_lista})
    else:
        return render(request, 'scolarte/listas/listas-de-usuario.html', {'listas':listas})




@csrf_exempt
def create_my_first_list_or_pass(request):
    user_lists = List.objects.filter(user=request.user)
    if not user_lists:
        print("No se encontró listas")
        lista = List.objects.create(name="Mi primera lista",
        user=request.user)
        return HttpResponse("Se creo primera lista de usuario")
    else:
        print("Se encontró listas")
        return HttpResponse("Ya existen lista(s) pertenecientes al usuario")


### Read CSV file to create models ###


# Create your views here.
# one parameter named request
def schools_upload(request):
    # declaring template
    template = "scolarte/escuelas/escuelas.html"
    data = School.objects.all()
    # prompt is a context variable that can have different values depending on their context
    prompt = {
        'orden': 'El orden de las columnas del archivo CSV debe ser: escuela, direccion, referencia, provincia, cantón, parroquia',
        'escuelas': data    
              }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)
    elif request.method == "POST":    
        csv_file = request.FILES['file']
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'El archivo no es un archivo CSV')
        data_set = csv_file.read().decode('iso-8859-1')
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            _, created = School.objects.update_or_create(
                name=column[0],
                address=column[1],
                address_reference=column[2],
                provincia=column[3],
                canton=column[4],
                parroquia=column[5],
            )
        context = {}
        return redirect('lists:schools_upload') 



def free_lists(request):
    free_lists = List.objects.filter(seller__isnull=True)
    return render(request, 'scolarte/listas/listas-libres.html', {'free_lists':free_lists})


@csrf_exempt
def assign_free_list_to_seller(request):
    
    seller_list_count = len(List.objects.filter(seller = request.user))

    if seller_list_count >= 10:
        response = JsonResponse({"error": "there was an error"})
        response.status_code = 403 # To announce that the user isn't allowed to publish
        return response
    else:    
        lista_id = request.POST.get('lista_id')
        try:
            lista = List.objects.get(id=lista_id)
            lista.seller = request.user
            lista.save()
        except Exception as e:
            raise e
        return redirect(reverse('lists:free_lists'))
            



    
     

