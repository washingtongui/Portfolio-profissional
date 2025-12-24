from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Contato
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.utils.html import strip_tags

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

            # 2. Tenta enviar o e-mail (Configurado para não travar o site)
            assunto_email = f"🚀 Novo Contato: {v_assunto}"
            html_content = f"<b>De:</b> {v_contato}<br><br><b>Mensagem:</b><br>{v_mensagem}"

            send_mail(
                subject=assunto_email,
                message=strip_tags(html_content),
                from_email=settings.EMAIL_HOST_USER,  # Seu Gmail (remetente)
                # Seu Gmail (destinatário)
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,  # Deixe False para capturarmos o erro real nos logs do Railway
                html_message=html_content,
            )

            messages.success(request, "Mensagem enviada com sucesso!")
            return redirect(request.path_info)

        except Exception as e:
            # Este erro aparecerá na aba 'Deploy Logs' do seu Railway
            print(f"--- ERRO DE ENVIO DE E-MAIL NO RAILWAY: {str(e)} ---")

            # Avisa o usuário que o dado foi salvo, mas o e-mail falhou
            messages.warning(
                request, "Sua mensagem foi salva no sistema, mas houve um atraso no aviso por e-mail.")
            return redirect(request.path_info)

    return render(request, 'contate-me.html')
