from django.contrib import admin
from django.urls import path, include, re_path
from core import views
from django.conf import settings
from django.conf.urls.static import static
#from roles.views import client, seller


# Change names
admin.site.site_header = "Escolart Administracion"
admin.site.site_title = "Escolate Portal Administrativo"
admin.site.index_title = "Welcome to Escolart Sitio Administrativo"

urlpatterns = [
    path('', include('core.urls')),
    path('cuentas/', include('roles.urls')),
    path('listas/', include('lists.urls')),
    path('productos/', include('products.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)