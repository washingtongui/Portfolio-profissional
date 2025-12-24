from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    # 1. Painel Administrativo.
    path('admin/', admin.site.urls),

    # 2. Página Inicial
    path('', views.index, name='index'),

    # 3. Página de Perfil
    path('perfil/', views.perfil, name='perfil'),

    # 4. Página de Projetos
    path('projetos/', views.projetos, name='projetos'),

    # 5. Página de Contato (Mantenha APENAS esta linha para o contato)
    path('contato/', views.contato_view, name='contato'),
]
