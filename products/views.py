from django.shortcuts import render
from .models import *
from lists.models import List
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView

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



def all_prod_by_category(request, c_slug=None):
    c_page = None
    products = None
    print("c_page is :", c_page)
    print("products is :", c_page)
    print("c_slug is :", c_slug)
    if c_slug != None:
        c_page = get_object_or_404(Category, slug=c_slug)
        print("category name is: ", c_page.name)
        products = Product.objects.filter(category=c_page, available=True)
    else:
        products = Product.objects.all().filter(available=True)
    return render(request, "scolarte/productos-por-categoria.html",
        {'category': c_page,
        'products': products}
    )



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
                category=filter_val,
            ).filter(available=True).order_by('-created_at')
            return context

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        context['filtro'] = self.request.GET.get('filtro', 'todas')
        context['orderby'] = self.request.GET.get('orderby', 'created_at')
        context['category'] = Category.objects.get(slug="cuadernos")
        context['total_products'] = Product.objects.filter(available=True).count()
        context['product_count_by_category'] = self.get_queryset().count()
        context['users_lists'] = List.objects.filter(user=self.request.user)
        
        return context
