from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contato
from django.utils import timezone
from datetime import timedelta

# --- PÁGINAS QUE JÁ EXISTIAM ---


def index(request):
    return render(request, 'index.html')


def perfil(request):
    return render(request, 'perfil.html')


def projetos(request):
    return render(request, 'projetos.html')

# --- LÓGICA DE CONTATO COM LIMITE DE ENVIOS ---


def contato_view(request):
    if request.method == 'POST':
        # 1. Captura os dados
        v_assunto = request.POST.get('assunto', '').strip()
        v_contato = request.POST.get('contato', '').strip()
        v_mensagem = request.POST.get('mensagem', '').strip()

        # --- BLOCO DE LIMITAÇÃO (Anti-Spam) ---
        # Define o limite de 3 mensagens a cada 24 horas por contato
        LIMITE_DIARIO = 3
        tempo_limite = timezone.now() - timedelta(hours=24)

        contagem_mensagens = Contato.objects.filter(
            contato_retorno=v_contato,
            data_envio__gte=tempo_limite
        ).count()

        if contagem_mensagens >= LIMITE_DIARIO:
            messages.error(
                request,
                "Você já enviou muitas mensagens hoje. Por favor, aguarde 24h para entrar em contato novamente."
            )
            return render(request, 'contate-me.html')
        # ---------------------------------------

        # 2. Validação de campos vazios
        if not v_assunto or not v_contato or not v_mensagem:
            messages.error(
                request, "Por favor, preencha todos os campos corretamente.")
            return render(request, 'contate-me.html')

        # 3. Validação de limites de caracteres
        if len(v_assunto) > 100 or len(v_mensagem) > 1000:
            messages.error(request, "Limite de caracteres excedido.")
            return render(request, 'contate-me.html')

        # 4. Tenta salvar no Banco de Dados
        try:
            Contato.objects.create(
                assunto=v_assunto,
                contato_retorno=v_contato,
                mensagem=v_mensagem
            )
            messages.success(
                request, "Sua mensagem foi enviada! Em breve entrarei em contato.")
            return redirect('contato')

        except Exception as e:
            messages.error(request, f"Ocorreu um erro ao salvar: {e}")
            return render(request, 'contate-me.html')

    return render(request, 'contate-me.html')
