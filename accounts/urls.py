"""
accounts/urls.py - Rotas do app de usuários
"""
from django.urls import path
from . import views

# Nome do app para referenciar nas templates (ex: {% url 'accounts:login' %})
app_name = 'accounts'

urlpatterns = [
    # Login e logout
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Gerenciamento de usuários (apenas admin)
    path('usuarios/', views.lista_usuarios_view, name='lista_usuarios'),
    path('usuarios/cadastrar/', views.cadastro_usuario_view, name='cadastrar_usuario'),
    path('usuarios/<int:pk>/editar/', views.editar_usuario_view, name='editar_usuario'),
    path('usuarios/<int:pk>/excluir/', views.excluir_usuario_view, name='excluir_usuario'),

    # Perfil do usuário logado
    path('perfil/', views.perfil_view, name='perfil'),
]
