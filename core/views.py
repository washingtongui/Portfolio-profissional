from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contato
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags

# --- NOVAS VIEWS PARA OS SEUS TEMPLATES ---


def index(request):
    return render(request, 'index.html')


def perfil(request):
    return render(request, 'perfil.html')


def projetos(request):
    return render(request, 'projetos.html')

# --- SUA VIEW DE CONTATO EXISTENTE ---


def contato_view(request):
    if request.method == 'POST':
        v_assunto = request.POST.get('assunto', '').strip()
        v_contato = request.POST.get('contato', '').strip()
        v_mensagem = request.POST.get('mensagem', '').strip()

        if not v_assunto or not v_contato or not v_mensagem:
            messages.error(request, "Por favor, preencha todos os campos.")
            return redirect(request.path_info)

        tempo_limite = timezone.now() - timedelta(hours=24)
        if Contato.objects.filter(contato_retorno=v_contato, data_envio__gte=tempo_limite).count() >= 3:
            messages.error(
                request, "Limite diário atingido. Tente novamente amanhã.")
            return redirect(request.path_info)

        try:
            Contato.objects.create(
                assunto=v_assunto,
                contato_retorno=v_contato,
                mensagem=v_mensagem
            )

            assunto_email = f"🚀 Novo Contato: {v_assunto}"
            html_content = f"<b>De:</b> {v_contato}<br><br><b>Mensagem:</b><br>{v_mensagem}"

            send_mail(
                subject=assunto_email,
                message=strip_tags(html_content),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=True,
                html_message=html_content,
            )

            messages.success(request, "Mensagem enviada com sucesso!")
            return redirect(request.path_info)

        except Exception:
            messages.warning(
                request, "Sua mensagem foi salva, mas o aviso por e-mail falhou.")
            return redirect(request.path_info)

    return render(request, 'contate-me.html')
