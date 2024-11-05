from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  
    path('artigo/', include('artigo.urls')),  # Inclui as URLs do app artigo
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('api/', include('api.urls')),  # Inclui as rotas da API
]

# Adiciona suporte para servir arquivos de mídia no modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
