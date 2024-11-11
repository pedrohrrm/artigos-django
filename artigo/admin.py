from django.contrib import admin
from .models import Artigo, Auditoria

@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'data', 'revista')
    search_fields = ('titulo', 'autores')

@admin.register(Auditoria)
class AuditoriaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'acao', 'data_hora', 'descricao')
    search_fields = ('usuario__username', 'acao')
    list_filter = ('acao', 'data_hora')