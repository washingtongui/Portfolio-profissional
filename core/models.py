from django.db import models


class Contato(models.Model):
    # Limite de 100 caracteres para o assunto
    assunto = models.CharField(max_length=100)
    # Limite de 150 para o contato (email/tel)
    contato_retorno = models.CharField(max_length=150)
    # Limite de 1000 para a mensagem
    mensagem = models.TextField(max_length=1000)
    data_envio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.assunto} - {self.contato_retorno}"
