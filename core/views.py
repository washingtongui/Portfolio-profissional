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
    return render(request, 'projetos.html')

# --- LÓGICA DE CONTATO (DESIGN AMPLO, JUSTIFICADO E NOMINAL) ---


def contato_view(request):
    if request.method == 'POST':
        # 1. Captura os dados
        v_assunto = request.POST.get('assunto', '').strip()
        v_contato = request.POST.get('contato', '').strip()
        v_mensagem = request.POST.get('mensagem', '').strip()

        # --- BLOCO ANTI-SPAM ---
        LIMITE_DIARIO = 3
        tempo_limite = timezone.now() - timedelta(hours=24)
        contagem_mensagens = Contato.objects.filter(
            contato_retorno=v_contato,
            data_envio__gte=tempo_limite
        ).count()

        if contagem_mensagens >= LIMITE_DIARIO:
            messages.error(
                request, "Limite diário atingido. Tente novamente em 24h.")
            return render(request, 'contate-me.html')

        # --- VALIDAÇÕES ---
        if not v_assunto or not v_contato or not v_mensagem:
            messages.error(
                request, "Por favor, preencha todos os campos corretamente.")
            return render(request, 'contate-me.html')

        try:
            # 2. Salva no Banco de Dados
            Contato.objects.create(
                assunto=v_assunto,
                contato_retorno=v_contato,
                mensagem=v_mensagem
            )

            # 3. Configura o E-mail HTML (Elegante, Largo e Justificado)
            assunto_email = f"🚀 Novo Contato: {v_assunto}"

            html_content = f"""
            <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #0d1117; padding: 40px 0;">
                <tr>
                    <td align="center">
                        <table width="700" border="0" cellspacing="0" cellpadding="0" style="background-color: #161b22; border: 1px solid #30363d; border-radius: 20px; overflow: hidden; box-shadow: 0 20px 50px rgba(0,0,0,0.6);">
                            
                            <tr>
                                <td align="center" style="background: linear-gradient(135deg, #007bff 0%, #00ffff 100%); padding: 50px;">
                                    <h1 style="margin: 0; font-family: 'Segoe UI', Arial, sans-serif; font-size: 30px; color: #ffffff; text-transform: uppercase; letter-spacing: 4px; font-weight: 800;">
                                        Novo Contato
                                    </h1>
                                </td>
                            </tr>

                            <tr>
                                <td style="padding: 60px; font-family: 'Segoe UI', Arial, sans-serif; color: #f0f6fc;">
                                    <p style="font-size: 22px; margin-bottom: 25px;">Olá, <strong style="color: #00ffff;">Washington</strong>!</p>
                                    <p style="font-size: 18px; color: #8b949e; line-height: 1.6; margin-bottom: 35px;">
                                        Você recebeu uma nova interação através do seu portfólio. Confira os detalhes:
                                    </p>
                                    
                                    <div style="background: rgba(255, 255, 255, 0.03); border: 1px solid #30363d; border-radius: 12px; padding: 30px; margin-bottom: 40px;">
                                        <p style="margin: 0 0 15px 0; font-size: 17px;">
                                            <strong style="color: #58a6ff;">📌 Assunto:</strong> 
                                            <span style="color: #f0f6fc;">{v_assunto}</span>
                                        </p>
                                        <p style="margin: 0; font-size: 17px;">
                                            <strong style="color: #58a6ff;">📧 Contato:</strong> 
                                            <a href="mailto:{v_contato}" style="color: #00ffff; text-decoration: none;">{v_contato}</a>
                                        </p>
                                    </div>

                                    <div style="background: #0d1117; padding: 40px; border-radius: 15px; border: 1px solid #30363d;">
                                        <p style="margin: 0 0 15px 0; color: #8b949e; font-size: 13px; text-transform: uppercase; font-weight: bold; letter-spacing: 1px;">Mensagem Recebida:</p>
                                        <div style="font-size: 18px; color: #c9d1d9; line-height: 1.8; text-align: justify; white-space: pre-line;">
                                            {v_mensagem}
                                        </div>
                                    </div>

                                    <div style="margin-top: 50px; text-align: center;">
                                        <a href="mailto:{v_contato}" style="background: #238636; color: #ffffff; padding: 20px 50px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 18px; display: inline-block;">
                                            Responder agora
                                        </a>
                                    </div>
                                </td>
                            </tr>

                            <tr>
                                <td align="center" style="background: #0d1117; padding: 30px; font-family: Arial, sans-serif; font-size: 13px; color: #484f58; border-top: 1px solid #30363d;">
                                    Notificação Automática • <strong>Washington Tom</strong> • 2025
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
            """

            text_content = strip_tags(html_content)

            # 4. Envio do E-mail
            send_mail(
                assunto_email,
                text_content,
                settings.EMAIL_HOST_USER,
                [settings.EMAIL_HOST_USER],
                fail_silently=False,
                html_message=html_content,
            )

            messages.success(
                request, "Sua mensagem foi enviada! Em breve entrarei em contato.")
            return redirect('contato')

        except Exception as e:
            messages.error(request, "Erro técnico ao processar contato.")
            print(f"Erro: {e}")
            return render(request, 'contate-me.html')

    return render(request, 'contate-me.html')
