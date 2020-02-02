from django.shortcuts import render, redirect
from .models import *
from lists.models import List
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
import csv, io
from django.contrib import messages
from django.views.generic.edit import UpdateView
from django.shortcuts import get_list_or_404, get_object_or_404
from django.db import IntegrityError

# Create your views here.


class AllCategories(TemplateView):
    template_name = "scolarte/categorias.html" 

    def get_context_data(self, **kwargs): 
        context = kwargs 
        context['categories'] = Category.objects.all()
        return context

    def get(self, request, *args, **kwargs): 
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)  




class ProductsListView(ListView):

    model = Product
    template_name = "scolarte/productos/productos.html"
    paginate_by = 9

    def get_queryset(self):
        filter_val = self.request.GET.get('filtro', 'todas')
        filter_val = filter_val.lower()
        order = self.request.GET.get('orderby', 'created_at')
        if filter_val == "todas":
            context = Product.objects.all().filter(available=True).order_by('-created_at')
            return context
        else:
            context = Product.objects.filter(
                category__slug=filter_val,
            ).filter(available=True).order_by('-created_at')
            return context    
           

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        try:
            selected_category = Category.objects.get(slug=self.request.GET.get('filtro', 'todas'))
        except Category.DoesNotExist:
            selected_category = None
        context['filtro'] = self.request.GET.get('filtro', 'todas')
        context['orderby'] = self.request.GET.get('orderby', 'created_at')
        context['categories'] = Category.objects.all()
        context['selected_category'] = selected_category
        context['total_products'] = Product.objects.filter(available=True).count()
        context['product_count_by_category'] = self.get_queryset().count()
        context['users_lists'] = List.objects.filter(user=self.request.user)
        
        return context




### Categorías Upload ###

# Create your views here.
# one parameter named request
def categories_upload(request):
    # declaring template
    template = "scolarte/categorias/subir-categorias.html"
    data = Category.objects.all()
    # prompt is a context variable that can have different values depending on their context
    prompt = {
        'orden': 'El orden de las columnas del archivo CSV debe ser: producto, direccion, referencia, provincia, cantón, parroquia',
        'categorias': data    
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
            try:
                _, created = Category.objects.update_or_create(
                    system_id=column[0],
                    name=column[1],
                    slug=column[2],
                    description=column[3],
                    image=column[4]
                )
            except IntegrityError as e: 
                if 'unique constraint' in e.args:
                    continue     
        context = {}
        return redirect('products:categories_upload') 



### SubCategorías Upload ###

# Create your views here.
# one parameter named request
def subcategories_upload(request):
    # declaring template
    template = "scolarte/subcategorias/subir-subcategorias.html"
    data = SubCategory.objects.all()# prompt is a context variable that can have different values depending on their context
    prompt = {
        'orden': 'El orden de las columnas del archivo CSV debe ser: producto, direccion, referencia, provincia, cantón, parroquia',
        'subcategorias': data    
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
            try:
                _, created = SubCategory.objects.update_or_create(
                    category=Category.objects.get(name=column[0]),
                    system_id=column[1],
                    name=column[2],
                    slug=column[3],
                    description=column[4],
                    image=column[5]
                )
            except IntegrityError as e: 
                if 'unique constraint' in e.args:
                    continue     
        context = {}
        return redirect('products:subcategories_upload') 



### MArcas Upload ###

# Create your views here.
# one parameter named request
def brands_upload(request):
    # declaring template
    template = "scolarte/marcas/subir-marcas.html"
    data = Brand.objects.all()# prompt is a context variable that can have different values depending on their context
    prompt = {
        'orden': 'El orden de las columnas del archivo CSV debe ser: producto, direccion, referencia, provincia, cantón, parroquia',
        'marcas': data    
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
            try:
                _, created = Brand.objects.update_or_create(
                    system_id=column[0],
                    name=column[1],
                    slug=column[2],
                    description=column[3],
                    image=column[4]
                )
            except IntegrityError as e: 
                if 'unique constraint' in e.args:
                    continue    
        context = {}
        return redirect('products:brands_upload') 





### Products Upload ###


# Create your views here.
# one parameter named request
def products_upload(request):
    # declaring template
    template = "scolarte/productos/subir-productos.html"
    data = Product.objects.all()
    # prompt is a context variable that can have different values depending on their context
    prompt = {
        'orden': 'El orden de las columnas del archivo CSV debe ser: producto, direccion, referencia, provincia, cantón, parroquia',
        'productos': data    
              }
    # GET request returns the value of the data with the specified key.
    if request.method == "GET":
        return render(request, template, prompt)
    elif request.method == "POST": 
        csv_file = request.FILES['file']
        if not csv_file:
            messages.error(request, 'Por favor, seleccione un archivo CSV')   
        # let's check if it is a csv file
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'El archivo no es un archivo CSV')
        data_set = csv_file.read().decode('iso-8859-1')
        # setup a stream which is when we loop through each line we are able to handle a data in a stream
        io_string = io.StringIO(data_set)
        next(io_string)
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            try:
                _, created = Product.objects.update_or_create(
                    category=Category.objects.get(name=column[0]),
                    subcategory=SubCategory.objects.get(system_id=column[1]),
                    brand=Brand.objects.get(name=column[2]),
                    system_id=column[3],
                    large_name=column[4],
                    short_name=column[5],
                    slug=column[6],
                    sku=column[7],
                    description=column[8],
                    price=column[9],
                    stock=column[10],
                    image=column[11],
                    available=column[12]
                )
            except IntegrityError as e: 
                if 'unique constraint' in e.args:
                    continue 
        context = {}
        return redirect('products:products_upload') 