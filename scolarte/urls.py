from django.contrib import admin
from django.urls import path, include, re_path
from core import views
from django.conf import settings
from django.conf.urls.static import static
#from roles.views import client, seller

urlpatterns = [
    path('', include('core.urls')),
    path('cuentas/', include('roles.urls')),
    path('listas/', include('lists.urls')),
    path('admin/', admin.site.urls),
    # path('productos/', include('products.urls')),
    # path('marcas/', include('brands.urls')),
    # path('list_de_utiles/', include('lists.urls')),
    #path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/signup/', entry.SignUpView.as_view(), name='signup'),
    # path('accounts/signup/cliente/', cliente.ClienteSignUpView.as_view(), name='cliente_signup'),
    # path('accounts/signup/vendedor/', vendedor.VendedorSignUpView.as_view(), name='vendedor_signup'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)