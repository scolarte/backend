from django.shortcuts import render
from .models import List, ListItem
from products.models import Product, ProductItem
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .forms import ListForm


# Create your views here.
### List Details ###

def full_remove_product(request, product_item_id):
    product_item = ProductItem.objects.get(id=product_item_id)
    product_item.delete()

    return redirect('listas:list_details') 


def list_details(request, lista_id, total=0, counter=0):
    
    try:
        #lista_id = request.COOKIES.get('lista_id')
        lista = List.objects.get(id=lista_id)
    except ObjectDoesNotExist:
        lista = List.objects.create(name="Lista anónima")
      
    list_items = ListItem.objects.filter(lista=lista)
    
    for list_item in list_items:
        total += Decimal(list_item.sub_total())

    return render(request, 'scolarte/listas/lista-detalles.html',
                  dict(lista = lista, list_items = list_items, total=total))




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
        lista = List.objects.create(name="Lista anónima",
        user=request.user)

    c_slug = request.POST.get('c_slug')
    s_slug = request.POST.get('s_slug')
    product_slug = request.POST.get('product_slug')
    
    try:

        product = Product.objects.get(
            category__slug=c_slug,
            subcategory__slug=s_slug,
            slug=product_slug)

        list_item = ListItem.objects.create(
            lista=lista,
            product=product,
            comment="")
       
        # response.set_cookie("lista_id", lista_id)
        # response.set_cookie("product_item_id", product_item.id)
        #return response
        return HttpResponse("post request success")
        

    except Exception as e:
        raise e




class AllLists(LoginRequiredMixin, TemplateView):
    template_name = "scolarte/listas.html" 
    login_url = '/ingresar/'
    redirect_field_name = 'redirect_to'

    def get_context_data(self, request, **kwargs): 
        context = kwargs
        context['listas'] = List.objects.filter(user=request.user)
        return context

    #To do
    #Append lists to user    

    def get(self, request, *args, **kwargs): 
        context = self.get_context_data(request, **kwargs)
        return self.render_to_response(context)  


@csrf_exempt
def update_lists_count(request):
    listas_de_usuario = List.objects.filter(user=request.user)
    if not listas_de_usuario:
        mi_primera_lista = List.objects.create(name="Mi primera lista",
        user=request.user)
        return render(request, 'scolarte/listas/listas-de-usuario.html', {'mi_primera_lista':mi_primera_lista})
    elif listas_de_usuario:
        return render(request, 'scolarte/listas/listas-de-usuario.html', {'listas':listas_de_usuario})




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
