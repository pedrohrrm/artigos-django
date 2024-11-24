from django.shortcuts import render
from django.http import JsonResponse
import logging
from django.views.decorators.csrf import csrf_exempt
import json


logger = logging.getLogger(__name__)


@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = request.body.decode('utf-8')
        message = json.loads(data).get('message', '').lower()

        # Lógica de palavras-chave
        if "artigo" in message:
            response = (
                "Você mencionou 'artigo'. O que você gostaria de fazer?<br>"
                "👉 Para **cadastrar um artigo**, digite 'cadastrar artigo'.<br>"
                "👉 Para **buscar um artigo**, digite 'buscar artigo'.<br>"
                "👉 Para **editar ou excluir um artigo**, digite 'editar artigo' ou 'excluir artigo'."
            )
        elif "cadastrar artigo" in message:
            response = (
                "Para cadastrar um artigo, acesse a página de cadastro ou forneça os detalhes diretamente.<br>"
                "Exemplo: 'Título, Autor, Resumo'."
            )
        elif "buscar artigo" in message:
            response = (
                "Para buscar um artigo, digite:<br>"
                "🔍 'buscar título &lt;título&gt;' para buscar por título.<br>"
                "🔍 'buscar autor &lt;nome&gt;' para buscar por autor.<br>"
                "🔍 'buscar palavra-chave &lt;palavra&gt;' para buscar por palavra-chave."
            )
        elif "editar" in message or "excluir" in message:
            response = (
                "Você mencionou 'editar' ou 'excluir' um artigo. O que você gostaria de fazer?<br>"
                "👉 Para **editar um artigo**, forneça os detalhes no formato:<br>"
                "🔧 'editar título &lt;novo título&gt;' para alterar o título.<br>"
                "🔧 'editar autor &lt;novo autor&gt;' para alterar o autor.<br>"
                "🔧 'editar resumo &lt;novo resumo&gt;' para alterar o resumo.<br><br>"
                "👉 Para **excluir um artigo**, use o comando:<br>"
                "❌ 'excluir artigo &lt;ID do artigo&gt;'.<br><br>"
                "Ou vá até a página de artigos e clique na opção correspondente para editar ou excluir diretamente."
            )
        elif "login" in message or "logout" in message:
            response = (
                "Para login, clique no botão de login no menu superior.<br>"
                "Para logout, clique no botão de logout no canto superior direito."
            )
        elif "ajuda" in message or "help" in message:
            response = (
                "Aqui estão algumas coisas que posso ajudar:<br>"
                "📝 Cadastrar artigos.<br>"
                "🔍 Buscar artigos por título, autor ou palavra-chave.<br>"
                "✏️ Editar ou excluir artigos.<br>"
                "🔐 Fazer login ou logout.<br>"
                "📜 Ver logs ou histórico.<br>"
                "❓ Precisa de algo mais? Basta perguntar!"
            )
        else:
            response = (
                "Desculpe, não entendi sua mensagem. Tente algo como:<br>"
                "👉 'artigo' para opções relacionadas a artigos.<br>"
                "👉 'ajuda' para obter uma lista de comandos disponíveis."
            )

        return JsonResponse({"response": response})

    return JsonResponse({"response": "Método inválido."})
def home(request):
    return render(request, 'home.html')

