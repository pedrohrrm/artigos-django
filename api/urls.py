from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import ArtigoViewSet

router = DefaultRouter()
router.register(r'artigos', ArtigoViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Inclui todas as rotas do ViewSet
]
