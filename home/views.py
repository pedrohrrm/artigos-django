from django.shortcuts import render
from django.http import JsonResponse
import logging
from django.views.decorators.csrf import csrf_exempt
import json


logger = logging.getLogger(__name__)


@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        # Parse da mensagem do usuário
        data = json.loads(request.body)
        user_message = data.get('message', '').lower()

        # Respostas predefinidas
        responses = {
            "cadastrar artigo": "Para cadastrar um artigo, acesse a aba 'Criar Artigo' no menu superior.",
            "login": "Você pode acessar a página de login no canto superior direito.",
            "buscar artigo": "Use a barra de busca para encontrar artigos pelo título, autor ou palavra-chave.",
            "ajuda": "Eu sou o chatbot! Posso ajudar você com navegação no site ou responder perguntas básicas.",
            "excluir artigo": "Você pode excluir um artigo clicando no botão 'Excluir' na página de detalhes do artigo.",
            "editar artigo": "Para editar um artigo, clique no botão 'Editar' na página de detalhes do artigo.",
            "download artigo": "Você pode fazer o download de um artigo clicando no botão 'Download' na página de detalhes.",
        }

        # Busca uma resposta correspondente
        response = responses.get(user_message, "Desculpe, não entendi sua pergunta. Tente perguntar de outra maneira.")

        # Retorna a resposta
        return JsonResponse({'response': response})

    return JsonResponse({'response': 'Método inválido.'}, status=405)

def home(request):
    
    return render(request, 'home.html')

