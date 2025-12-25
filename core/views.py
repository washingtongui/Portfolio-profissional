import resend  # Certifique-se de ter rodado 'pip install resend'
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

# --- VIEW DE CONTATO COM DESIGN AMPLO E TEXTO GRANDE ---


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
            # 1. Salva no Banco de Dados
            Contato.objects.create(
                assunto=v_assunto,
                contato_retorno=v_contato,
                mensagem=v_mensagem
            )

            # --- CONFIGURAÇÃO E ENVIO VIA RESEND ---
            resend.api_key = settings.RESEND_API_KEY

            params = {
                "from": settings.DEFAULT_FROM_EMAIL,
                "to": ["washingtongui678@gmail.com"],
                "subject": f"🚀 Novo Contato: {v_assunto}",
                "html": f"""
                <div style="background-color: #12151c; padding: 50px 20px; font-family: 'Segoe UI', Arial, sans-serif; text-align: center;">
                    <div style="max-width: 650px; margin: 0 auto; background-color: #1c222d; border-radius: 24px; overflow: hidden; color: #ffffff; text-align: left; box-shadow: 0 10px 40px rgba(0,0,0,0.4);">
                        
                        <div style="background: linear-gradient(135deg, #007bff, #00f2fe); padding: 60px 40px; text-align: center;">
                            <h1 style="margin: 0; font-size: 36px; letter-spacing: 4px; text-transform: uppercase; font-weight: 800; line-height: 1.1; color: #ffffff;">
                                NOVO<br>ALERTA DE<br>CONTATO
                            </h1>
                        </div>

                        <div style="padding: 50px 50px;">
                            <p style="font-size: 24px; margin-bottom: 25px; font-weight: 600;">Olá Tom,</p>
                            
                            <p style="font-size: 19px; color: #a0a6b5; line-height: 1.8; margin-bottom: 40px;">
                                Você recebeu uma nova mensagem através do seu formulário de portfólio. Confira os detalhes abaixo:
                            </p>

                            <div style="border-left: 6px solid #00f2fe; padding-left: 30px; margin-bottom: 45px;">
                                <p style="margin: 0 0 25px 0; font-size: 19px; line-height: 1.6;">
                                    <strong style="color: #00f2fe; text-transform: uppercase; font-size: 14px; letter-spacing: 1px;">Assunto:</strong><br>
                                    <span style="font-size: 22px; font-weight: bold;">{v_assunto}</span>
                                </p>
                                <p style="margin: 0; font-size: 19px; line-height: 1.6;">
                                    <strong style="color: #00f2fe; text-transform: uppercase; font-size: 14px; letter-spacing: 1px;">E-mail de Retorno:</strong><br>
                                    <a href="mailto:{v_contato}" style="color: #4da3ff; text-decoration: none; font-size: 20px; font-weight: bold; border-bottom: 1px solid #4da3ff;">{v_contato}</a>
                                </p>
                            </div>

                            <div style="background-color: #252c39; padding: 40px; border-radius: 18px; border: 1px solid #333d4f;">
                                <p style="margin: 0 0 15px 0; color: #00f2fe; font-weight: bold; font-size: 16px; text-transform: uppercase; letter-spacing: 1px;">
                                    Mensagem:
                                </p>
                                <p style="margin: 0; font-style: italic; color: #ffffff; line-height: 1.9; font-size: 20px;">
                                    "{v_mensagem}"
                                </p>
                            </div>

                            <div style="margin-top: 60px; text-align: center; border-top: 1px solid #333d4f; padding-top: 30px;">
                                 <p style="font-size: 14px; color: #5d6675; letter-spacing: 1px;">ENVIADO PELO SEU SISTEMA DE PORTFÓLIO</p>
                            </div>
                        </div>
                    </div>
                </div>
                """,
            }

            resend.Emails.send(params)

            messages.success(request, "Mensagem enviada com sucesso!")
            return redirect(request.path_info)

        except Exception as e:
            print(f"--- ERRO DE ENVIO VIA RESEND NO RAILWAY: {str(e)} ---")
            messages.warning(
                request, "Sua mensagem foi salva, mas houve um erro ao enviar o alerta por e-mail.")
            return redirect(request.path_info)

    return render(request, 'contate-me.html')
