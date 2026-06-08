"""
urls.py - Rotas principais do sistema
Aqui definimos quais endereços (URLs) levam para quais partes do sistema
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Painel administrativo do Django (acesso em /admin/)
    path('admin/', admin.site.urls),

    # Redireciona a raiz para o dashboard
    path('', include('core.urls')),

    # Rotas de autenticação (login, logout, cadastro)
    path('accounts/', include('accounts.urls')),

    # Rotas de fornecedores
    path('fornecedores/', include('fornecedores.urls')),

    # Rotas de produtos
    path('produtos/', include('produtos.urls')),

    # Rotas de movimentações
    path('movimentacoes/', include('movimentacoes.urls')),

    # Rotas de relatórios
    path('relatorios/', include('relatorios.urls')),
]

# Em desenvolvimento, serve os arquivos de mídia (imagens enviadas pelo usuário)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
