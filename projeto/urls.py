from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('index.urls')),
    path('financeiro/', include('financeiro.urls')),
    path('suprimentos/', include('suprimentos.urls')),
    path('estoque/', include('estoque.urls')),
    path('comercial/', include('comercial.urls')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
