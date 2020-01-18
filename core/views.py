from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import TemplateView
from products.models import Category, SubCategory, Brand, Product


# Create your views here.

def index(request):
    return HttpResponse("You're looking at question")


class ScolarteHome(TemplateView):
    template_name = "scolarte/index.html"



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