import resend  # Importante: certifique-se de ter rodado 'pip install resend'
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contato
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

# --- VIEWS DAS PÁGINAS DO PORTFÓLIO ---


def index(request):
    """Renderiza a página inicial."""
    return render(request, 'index.html')


def perfil(request):
    """Renderiza a página de perfil/sobre."""
    return render(request, 'perfil.html')


def projetos(request):
    """Renderiza a página de projetos."""
    return render(request, 'projetos.html')

# --- VIEW DE CONTATO COM LOG DE ERRO PARA PRODUÇÃO ---


def contato_view(request):
    if request.method == 'POST':
        v_assunto = request.POST.get('assunto', '').strip()
        v_contato = request.POST.get('contato', '').strip()
        v_mensagem = request.POST.get('mensagem', '').strip()

        # Validação básica
        if not v_assunto or not v_contato or not v_mensagem:
            messages.error(request, "Por favor, preencha todos os campos.")
            return redirect(request.path_info)

        # Anti-spam: Máximo 3 mensagens por contato em 24h
        tempo_limite = timezone.now() - timedelta(hours=24)
        if Contato.objects.filter(contato_retorno=v_contato, data_envio__gte=tempo_limite).count() >= 3:
            messages.error(
                request, "Limite diário atingido. Tente novamente amanhã.")
            return redirect(request.path_info)

        try:
            # 1. Salva no Banco de Dados (Sempre primeiro)
            Contato.objects.create(
                assunto=v_assunto,
                contato_retorno=v_contato,
                mensagem=v_mensagem
            )

            # --- CONFIGURAÇÃO DO RESEND ---
            # Puxa a chave da variável de ambiente definida no seu settings.py
            resend.api_key = settings.RESEND_API_KEY

            # 2. Envia o e-mail via API (Railway permite essa conexão)
            params = {
                "from": settings.DEFAULT_FROM_EMAIL,  # "onboarding@resend.dev"
                "to": ["washingtongui678@gmail.com"],  # Seu e-mail de destino
                "subject": f"🚀 Novo Contato: {v_assunto}",
                "html": f"""
                    <h3>Novo contato do seu Portfólio</h3>
                    <p><b>De:</b> {v_contato}</p>
                    <p><b>Assunto:</b> {v_assunto}</p>
                    <hr>
                    <p><b>Mensagem:</b></p>
                    <p>{v_mensagem}</p>
                """,
            }

            resend.Emails.send(params)

            messages.success(request, "Mensagem enviada com sucesso!")
            return redirect(request.path_info)

        except Exception as e:
            # Este erro aparecerá na aba 'Deploy Logs' do seu Railway
            print(f"--- ERRO DE ENVIO VIA RESEND NO RAILWAY: {str(e)} ---")

            # Avisa o usuário que o dado foi salvo, mas o e-mail falhou
            messages.warning(
                request, "Sua mensagem foi salva no sistema, mas houve um erro ao enviar o alerta por e-mail.")
            return redirect(request.path_info)

    return render(request, 'contate-me.html')
