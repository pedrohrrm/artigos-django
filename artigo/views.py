from datetime import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.http import FileResponse, Http404
import mimetypes
import os
import logging
from .forms import ArtigoForm, ConfirmacaoExclusaoForm, UserRegistrationForm
from .models import Artigo
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required



logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    return render(request, 'home.html')

@login_required
@permission_required('artigo.change_artigo', raise_exception=True)
def criar(request):
    if request.method == 'POST':
        form = ArtigoForm(request.POST, request.FILES)  # Inclua request.FILES para lidar com uploads
        if form.is_valid():
            form.save()  # Salva o artigo e o arquivo
            logger.info(f"Foi criado um artigo por {request.user.username}")
            return redirect('lista_artigos')  # Redireciona para a lista de artigos após o salvamento
    else:
        form = ArtigoForm()
    
    return render(request, 'criar.html', {'form': form})

@login_required
def lista_artigos(request):
    # Obtém os filtros e a ordenação
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

    # Ordena os resultados
    artigos = artigos.order_by(ordenar_por)

    # Pagina os resultados
    paginator = Paginator(artigos, 10)  # 10 artigos por página
    artigos_paginados = paginator.get_page(pagina)

    return render(request, 'lista_artigos.html', {
        'artigos': artigos_paginados,
        'filtros': filtros,
        'ordenar_por': ordenar_por
    })

@login_required
@permission_required('artigo.change_artigo', raise_exception=True)
def editar(request, artigo_id):
    artigo = get_object_or_404(Artigo, pk=artigo_id)

    if request.user != artigo.autor and not request.user.has_perm('app.change_artigo'):
        return HttpResponse("Você não tem permissão para editar este artigo.")
    
    if request.method == 'POST':
        form = ArtigoForm(request.POST, instance=artigo)
        if form.is_valid():
            form.save()
            logger.info(f"Artigo editado por {request.user.username} - ID: {artigo.id}")
            return redirect('detalhes_artigo', artigo_id=artigo_id)  # ou outra página de sucesso
    else:
        form = ArtigoForm(instance=artigo)
    return render(request, 'editar.html', {'form': form, 'artigo': artigo})

@login_required
def detalhes_artigo(request, artigo_id):
    artigo = get_object_or_404(Artigo, pk=artigo_id)
    return render(request, 'detalhes_artigo.html', {'artigo': artigo})

@login_required
def download_artigo(request, artigo_id):
    artigo = get_object_or_404(Artigo, pk=artigo_id)

    # Verifica se o arquivo existe
    if artigo.arquivo and artigo.arquivo.storage.exists(artigo.arquivo.name):
        # Obtém o caminho absoluto do arquivo
        file_path = artigo.arquivo.path
        
        # Obtém o tipo MIME do arquivo
        mime_type, _ = mimetypes.guess_type(file_path)
        if mime_type is None:
            mime_type = 'application/octet-stream'

        # Prepara a resposta para o arquivo
        response = FileResponse(open(file_path, 'rb'), content_type=mime_type)
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
        logger.info(f"Artigo baixado por {request.user.username} - ID: {artigo.id}")
        return response
    else:
        # Caso o arquivo não exista, renderiza um template de erro
        raise Http404("Arquivo não encontrado")

@login_required
@permission_required('artigo.change_artigo', raise_exception=True)  
def excluir_artigo(request, artigo_id):
    # Obtém o objeto Artigo ou retorna 404 se não encontrado
    artigo = get_object_or_404(Artigo, pk=artigo_id)


    if artigo.arquivo:
        arquivo_path = artigo.arquivo.path
        
        if os.path.exists(arquivo_path):
            try:
                os.remove(arquivo_path)
            except OSError as e:
                print(f"Erro ao remover o arquivo: {e}")
                return redirect('lista_artigos')

        # Remove a referência ao arquivo do banco de dados, mas não salva o objeto ainda
        artigo.arquivo.delete(save=False)
        
        # Salva o artigo sem o arquivo associado
        artigo.save()

    # Remove o artigo do banco de dados
    artigo.delete()
    logger.info(f"Artigo excluído por {request.user.username} - ID: {artigo_id}")

    # Redireciona para a página de lista de artigos após a exclusão
    return redirect('lista_artigos')  

from django.shortcuts import render
from .models import Artigo

@login_required
def busca_artigos(request):
    filtros = {
        'criterio': request.GET.get('criterio', ''),
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

    # Filtrando os artigos baseado no critério selecionado
    if filtros['criterio'] == 'titulo' and filtros['titulo']:
        artigos = artigos.filter(titulo__icontains=filtros['titulo'])
    elif filtros['criterio'] == 'autores' and filtros['autores']:
        artigos = artigos.filter(autores__icontains=filtros['autores'])
    elif filtros['criterio'] == 'revista' and filtros['revista']:
        artigos = artigos.filter(revista__icontains=filtros['revista'])
    elif filtros['criterio'] == 'palavras_chave' and filtros['palavras_chave']:
        artigos = artigos.filter(palavras_chave__icontains=filtros['palavras_chave'])
    elif filtros['criterio'] == 'data' and filtros['data']:
        artigos = artigos.filter(data=filtros['data'])
    elif filtros['criterio'] == 'resumo' and filtros['resumo']:
        artigos = artigos.filter(resumo__icontains=filtros['resumo'])

    # Ordenação
    artigos = artigos.order_by(ordenar_por)

    # Paginação
    from django.core.paginator import Paginator
    paginator = Paginator(artigos, 10)  # 10 artigos por página
    artigos_pag = paginator.get_page(pagina)

    context = {
        'filtros': filtros,
        'artigos': artigos_pag,
        'ordenar_por': ordenar_por,
    }
    return render(request, 'lista_artigos.html', context)


def criar_usuario(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return HttpResponse("Usuário criado com sucesso")


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Salva o novo usuário no banco de dados
            return redirect('login')  # Redireciona para a página de login
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

# View de Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redireciona para a página inicial ou outra página
        else:
            return render(request, 'login.html', {'error': 'Credenciais inválidas'})
    return render(request, 'login.html')

# View de Logout
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')