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
            return redirect('contato')

        # --- BLOCO ANTI-SPAM ---
        tempo_limite = timezone.now() - timedelta(hours=24)
        contagem_mensagens = Contato.objects.filter(
            contato_retorno=v_contato,
            data_envio__gte=tempo_limite
        ).count()

        if contagem_mensagens >= 3:
            messages.error(
                request, "Limite diário atingido. Tente novamente em 24h.")
            return redirect('contato')

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
            <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #0d1117; padding: 40px 0;">
                <tr>
                    <td align="center">
                        <table width="700" border="0" cellspacing="0" cellpadding="0" style="background-color: #161b22; border: 1px solid #30363d; border-radius: 20px; overflow: hidden;">
                            <tr>
                                <td align="center" style="background: linear-gradient(135deg, #007bff 0%, #00ffff 100%); padding: 50px;">
                                    <h1 style="margin: 0; font-family: Arial; color: #ffffff;">NOVO CONTATO</h1>
                                </td>
                            </tr>
                            <tr>
                                <td style="padding: 60px; font-family: Arial; color: #f0f6fc;">
                                    <p style="font-size: 20px;">Olá, <strong>Washington</strong>!</p>
                                    <p><strong>Assunto:</strong> {v_assunto}</p>
                                    <p><strong>Contato:</strong> {v_contato}</p>
                                    <hr style="border: 0; border-top: 1px solid #30363d; margin: 20px 0;">
                                    <p style="line-height: 1.6; text-align: justify;">{v_mensagem}</p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
            """
            text_content = strip_tags(html_content)

            # 4. Envio do E-mail (fail_silently=True impede o Erro 500)
            send_mail(
                assunto_email,
                text_content,
                settings.EMAIL_HOST_USER,
                ['washingtongui678@gmail.com'],
                fail_silently=True,
                html_message=html_content,
            )

            messages.success(
                request, "Sua mensagem foi enviada! Em breve entrarei em contato.")
            return redirect('contato')

        except Exception as e:
            print(f"Erro técnico: {e}")
            messages.error(request, "Erro ao processar sua mensagem.")
            return redirect('contato')

    return render(request, 'contate-me.html')
