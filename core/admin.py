from django.contrib import admin
from .models import Contato


@admin.register(Contato)
class ContatoAdmin(admin.ModelAdmin):
    # As colunas que vão aparecer na lista principal
    list_display = ('assunto', 'contato_retorno', 'data_envio')

    # Adiciona uma barra de pesquisa para filtrar por assunto ou contato
    search_fields = ('assunto', 'contato_retorno')

    # Adiciona um filtro lateral por data
    list_filter = ('data_envio',)

    # Ordena para que as mensagens mais recentes apareçam primeiro
    ordering = ('-data_envio',)

    # Deixa os campos apenas para leitura no painel para evitar alterações acidentais
    readonly_fields = ('assunto', 'contato_retorno', 'mensagem', 'data_envio')
