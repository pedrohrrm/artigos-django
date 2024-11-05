from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.shortcuts import get_object_or_404
from django.http import FileResponse, Http404
from django.core.paginator import Paginator
from artigo.models import Artigo  # Mantém a importação do modelo Artigo
from api.serializers import ArtigoSerializer  # Ajuste para o caminho correto do serializer
import os
import mimetypes


class ArtigoViewSet(viewsets.ModelViewSet):
    queryset = Artigo.objects.all()
    serializer_class = ArtigoSerializer
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated]

    # Criar artigo
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # Listar artigos com filtros
    def list(self, request, *args, **kwargs):
        filtros = {
            'titulo': request.GET.get('titulo', ''),
            'autor': request.GET.get('autor', ''),
            'revista': request.GET.get('revista', ''),
            'palavra_chave': request.GET.get('palavra_chave', ''),
            'data': request.GET.get('data', ''),
            'resumo': request.GET.get('resumo', '')
        }

        ordenar_por = request.GET.get('ordenar_por', 'data')
        pagina = request.GET.get('pagina', 1)

        artigos = Artigo.objects.all()

        # Aplica os filtros
        if filtros['titulo']:
            artigos = artigos.filter(titulo__icontains=filtros['titulo'])
        if filtros['autor']:
            artigos = artigos.filter(autores__icontains=filtros['autor'])
        if filtros['revista']:
            artigos = artigos.filter(revista__icontains=filtros['revista'])
        if filtros['palavra_chave']:
            artigos = artigos.filter(palavras_chave__icontains=filtros['palavra_chave'])
        if filtros['data']:
            artigos = artigos.filter(data=filtros['data'])
        if filtros['resumo']:
            artigos = artigos.filter(resumo__icontains=filtros['resumo'])

        # Ordena e pagina os resultados
        artigos = artigos.order_by(ordenar_por)
        paginator = Paginator(artigos, 10)
        artigos_paginados = paginator.get_page(pagina)

        serializer = self.get_serializer(artigos_paginados, many=True)
        return Response(serializer.data)

    # Detalhes de um artigo
    def retrieve(self, request, pk=None):
        artigo = get_object_or_404(Artigo, pk=pk)
        serializer = self.get_serializer(artigo)
        return Response(serializer.data)

    # Editar artigo
    def update(self, request, pk=None, *args, **kwargs):
        artigo = get_object_or_404(Artigo, pk=pk)
        serializer = self.get_serializer(artigo, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # Excluir artigo
    def destroy(self, request, pk=None):
        artigo = get_object_or_404(Artigo, pk=pk)
        if artigo.arquivo and os.path.exists(artigo.arquivo.path):
            os.remove(artigo.arquivo.path)
        artigo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # Ação personalizada para Download de arquivo
    @action(detail=True, methods=['get'])
    def download(self, request, pk=None):
        artigo = get_object_or_404(Artigo, pk=pk)
        if artigo.arquivo and artigo.arquivo.storage.exists(artigo.arquivo.name):
            file_path = artigo.arquivo.path
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type is None:
                mime_type = 'application/octet-stream'

            response = FileResponse(open(file_path, 'rb'), content_type=mime_type)
            response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return response
        else:
            raise Http404("Arquivo não encontrado")

    # Busca de artigos
    @action(detail=False, methods=['get'])
    def search(self, request):
        criterio = request.GET.get('criterio', '')
        filtros = {
            'titulo': request.GET.get('titulo', ''),
            'autores': request.GET.get('autores', ''),
            'revista': request.GET.get('revista', ''),
            'palavras_chave': request.GET.get('palavras_chave', ''),
            'data': request.GET.get('data', ''),
            'resumo': request.GET.get('resumo', ''),
        }
        ordenar_por = request.GET.get('ordenar_por', 'data')
        pagina = request.GET.get('pagina', 1)

        artigos = Artigo.objects.all()

        # Filtra artigos com base no critério
        if criterio == 'titulo' and filtros['titulo']:
            artigos = artigos.filter(titulo__icontains=filtros['titulo'])
        elif criterio == 'autores' and filtros['autores']:
            artigos = artigos.filter(autores__icontains=filtros['autores'])
        elif criterio == 'revista' and filtros['revista']:
            artigos = artigos.filter(revista__icontains=filtros['revista'])
        elif criterio == 'palavras_chave' and filtros['palavras_chave']:
            artigos = artigos.filter(palavras_chave__icontains=filtros['palavras_chave'])
        elif criterio == 'data' and filtros['data']:
            artigos = artigos.filter(data=filtros['data'])
        elif criterio == 'resumo' and filtros['resumo']:
            artigos = artigos.filter(resumo__icontains=filtros['resumo'])

        # Ordena e pagina os resultados
        artigos = artigos.order_by(ordenar_por)
        paginator = Paginator(artigos, 10)
        artigos_paginados = paginator.get_page(pagina)

        serializer = self.get_serializer(artigos_paginados, many=True)
        return Response(serializer.data)
