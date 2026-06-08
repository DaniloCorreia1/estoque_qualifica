"""
urls.py - Rotas principais do sistema
Aqui definimos quais endereços (URLs) levam para quais partes do sistema
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.http import FileResponse, Http404
import os


def servir_sw(request):
    """
    Serve o Service Worker na raiz /sw.js
    ESSENCIAL para o PWA funcionar — o SW precisa estar na raiz do site
    para ter escopo sobre todas as páginas.
    """
    sw_path = os.path.join(settings.BASE_DIR, 'static', 'sw.js')
    if not os.path.exists(sw_path):
        raise Http404("sw.js não encontrado")
    response = FileResponse(
        open(sw_path, 'rb'),
        content_type='application/javascript; charset=utf-8'
    )
    # Sem cache — o browser precisa sempre verificar a versão mais nova
    response['Service-Worker-Allowed'] = '/'
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response


urlpatterns = [
    # Service Worker na raiz — OBRIGATÓRIO para PWA funcionar corretamente
    path('sw.js', servir_sw, name='service_worker'),

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