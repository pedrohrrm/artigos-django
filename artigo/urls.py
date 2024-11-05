from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    # Rotas do frontend
    path('', views.home, name='home'),
    path('criar/', login_required(permission_required('app.add_artigo', raise_exception=True)(views.criar)), name='criar'),  
    path('lista_artigos/', views.lista_artigos, name='lista_artigos'),
    path('artigos/<int:artigo_id>/editar/', login_required(permission_required('app.change_artigo', raise_exception=True)(views.editar)), name='editar'),
    path('detalhes/<int:artigo_id>/', views.detalhes_artigo, name='detalhes_artigo'),
    path('download_artigo/<int:artigo_id>/', views.download_artigo, name='download_artigo'),
    path('excluir_artigo/<int:artigo_id>/', login_required(permission_required('app.delete_artigo', raise_exception=True)(views.excluir_artigo)), name='excluir_artigo'),
    path('busca/', views.busca_artigos, name='busca_artigos'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout')
]