from django.shortcuts import render
from .models import *

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
    template_name = "shop/catalogo.html"
    paginate_by = 9

    def get_queryset(self):
        filter_val = self.request.GET.get('filtro', 'todas')
        filter_val = filter_val.lower()
        order = self.request.GET.get('orderby', 'created')
        if filter_val == "todas":
            context = UnitaryProduct.objects.all().filter(available=True).order_by('-created')
            return context
        else:    
            context = UnitaryProduct.objects.filter(
                subcategory2=filter_val,
            ).filter(available=True).order_by('-created')
            return context

    def get_context_data(self, **kwargs):
        context = super(CatalogoListView, self).get_context_data(**kwargs)
        context['filtro'] = self.request.GET.get('filtro', 'todas')
        context['orderby'] = self.request.GET.get('orderby', 'created')
        context['category'] = Category.objects.get(slug="catalogo")
        context['total_stickers'] = UnitaryProduct.objects.filter(available=True).count()
        context['product_count'] = self.get_queryset().count()
        
        return context
