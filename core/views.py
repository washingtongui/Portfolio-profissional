from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contato
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags

# --- PÁGINAS EXISTENTES ---


def index(request):
    return render(request, 'index.html')


def perfil(request):
    return render(request, 'perfil.html')


def projetos(request):
    return render(request, 'projects.html')

# --- LÓGICA DE CONTATO ---


def contato_view(request):
    if request.method == 'POST':
        # 1. Captura os dados
        v_assunto = request.POST.get('assunto', '').strip()
        v_contato = request.POST.get('contato', '').strip()
        v_mensagem = request.POST.get('mensagem', '').strip()

        # --- VALIDAÇÕES ---
        if not v_assunto or not v_contato or not v_mensagem:
            messages.error(
                request, "Por favor, preencha todos os campos corretamente.")
            return redirect(request.path_info)

        # --- BLOCO ANTI-SPAM (3 mensagens em 24h) ---
        tempo_limite = timezone.now() - timedelta(hours=24)
        contagem = Contato.objects.filter(
            contato_retorno=v_contato,
            data_envio__gte=tempo_limite
        ).count()

        if contagem >= 3:
            messages.error(
                request, "Limite diário atingido. Tente novamente em 24h.")
            return redirect(request.path_info)

        try:
            # 2. Salva no Banco de Dados
            Contato.objects.create(
                assunto=v_assunto,
                contato_retorno=v_contato,
                mensagem=v_mensagem
            )

            # 3. Configura o E-mail HTML
            assunto_email = f"🚀 Novo Contato: {v_assunto}"
            html_content = f"""
            <div style="font-family: Arial, sans-serif; background-color: #0d1117; color: #f0f6fc; padding: 20px;">
                <h2 style="color: #007bff;">Novo Contato Recebido</h2>
                <p><strong>De:</strong> {v_contato}</p>
                <p><strong>Assunto:</strong> {v_assunto}</p>
                <div style="background: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d;">
                    {v_mensagem}
                </div>
            </div>
            """
            text_content = strip_tags(html_content)

            # 4. Envio do E-mail (Blindado com fail_silently)
            # Usamos settings.EMAIL_HOST_USER para garantir que o remetente seja o autenticado
            send_mail(
                subject=assunto_email,
                message=text_content,
                from_email=settings.EMAIL_HOST_USER,
                # Envia para você mesmo
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=True,  # Crucial: impede erro 500 se o Gmail bloquear o Railway
                html_message=html_content,
            )

            messages.success(
                request, "Sua mensagem foi enviada! Em breve entrarei em contato.")
            return redirect(request.path_info)

        except Exception as e:
            print(f"Erro ao processar contato: {e}")
            messages.error(
                request, "Houve um erro técnico, mas sua mensagem foi gravada.")
            return redirect(request.path_info)

    return render(request, 'contate-me.html')
