from django.shortcuts import render


def index(request):
    return render(request, 'index.html')


def perfil(request):
    return render(request, 'perfil.html')


def projetos(request):
    return render(request, 'MeusProjetos.html')


def contato(request):
    return render(request, 'contate-me.html')
