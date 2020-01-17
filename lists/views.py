from django.shortcuts import render
from .models import List, ListItem
from products.models import Product, ProductItem
from django.views.generic import TemplateView

# Create your views here.
### List Details ###

def full_remove_product(request, product_item_id):
    product_item = ProductItem.objects.get(id=product_item_id)
    product_item.delete()

    return redirect('listas:list_details') 


def list_details(request, total=0, counter=0, cart_items=None):
    
    try:
        lista_id = request.COOKIES.get('lista_id')
        lista = List.objects.get(lista_id=lista_id)
    except ObjectDoesNotExist:
        lista = List.objects.create(lista_id="Random")
      
    list_items = ListItem.objects.filter(lista=lista)
    
    for list_item in list_items:
        total += Decimal(list_item.sub_total())



    categories = Category.objects.exclude(name='Muestras')

    

    ### Calcular costo despacho ###

    
    costo_despacho = 15

    total_a_pagar = Decimal(total) + Decimal(costo_despacho)

    return render(request, 'cart.html',
                    dict(cart_items=cart_items, sample_items=sample_items, pack_items = pack_items, packs_with_min_prices = packs_with_min_prices, descuento = descuento,
                    descuento_packs_3x2 = descuento_packs_3x2, unitary_product_items = unitary_product_items, total=total, free_shipping_min_amount = free_shipping_min_amount,
                    counter=counter, categories=categories, total_a_pagar=total_a_pagar, descuento_por_cupon=descuento_por_cupon, costo_despacho=costo_despacho))





def add_product_to_list(request):

    lista_id = request.COOKIES.get('lista_id')
    if lista_id:
        lista = List.objects.get(id=lista_id)
    else:
        lista = List.objects.create(lista_id="Random")
        lista_id = lista.id

    c_slug = request.POST.get('c_slug')
    s_slug = request.POST.get('s_slug')
    product_slug = request.POST.get('product_slug')
    
    try:

        product = Product.objects.get(
            category__slug=c_slug,
            subcategory__slug=s_slug,
            slug=product_slug)

        product_item = ProductItem.objects.create(
            lista=lista,
            product=product,
            comment="")
       
        
        product_items_count = ProductItem.objects.filter(cart_id=cart_id).count()

        total_items = product_items_count

        response = JsonResponse({'list_items_counter':total_items})
        response.set_cookie("lista_id", lista_id)
        response.set_cookie("product_item_id", product_item.id)

        return response

    except Exception as e:
        raise e




class AllLists(TemplateView):
    template_name = "scolarte/listas.html" 

    def get_context_data(self, **kwargs): 
        context = kwargs 
        context['listas'] = List.objects.all()
        return context

    #To do
    #Append lists to user    

    def get(self, request, *args, **kwargs): 
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)  