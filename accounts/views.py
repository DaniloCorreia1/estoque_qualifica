"""
accounts/views.py - Views de autenticação e gerenciamento de usuários
Cada função/classe aqui responde a uma URL e retorna uma página HTML
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Usuario
from .forms import LoginForm, CadastroUsuarioForm, EdicaoUsuarioForm


def login_view(request):
    """
    Tela de login do sistema.
    Se o usuário já estiver logado, redireciona para o dashboard.
    """
    # Se já está logado, vai direto para o dashboard
    if request.user.is_authenticated:
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            # Pega os dados do formulário
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # Verifica usuário e senha no banco de dados
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  # Faz o login (cria a sessão)
                messages.success(request, f'Bem-vindo, {user.nome_exibicao}!')
                return redirect('core:dashboard')
            else:
                messages.error(request, 'Usuário ou senha incorretos.')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    """Faz o logout e redireciona para a tela de login"""
    logout(request)
    messages.info(request, 'Você saiu do sistema.')
    return redirect('accounts:login')


@login_required
def cadastro_usuario_view(request):
    """
    Tela de cadastro de novo usuário.
    Apenas administradores podem cadastrar novos usuários.
    """
    # Apenas admins podem cadastrar usuários
    if not request.user.is_admin:
        messages.error(request, 'Você não tem permissão para cadastrar usuários.')
        return redirect('core:dashboard')

    if request.method == 'POST':
        form = CadastroUsuarioForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = form.save()
            messages.success(request, f'Usuário {usuario.username} cadastrado com sucesso!')
            return redirect('accounts:lista_usuarios')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = CadastroUsuarioForm()

    return render(request, 'accounts/cadastro_usuario.html', {'form': form})


@login_required
def lista_usuarios_view(request):
    """
    Lista todos os usuários cadastrados no sistema.
    Apenas administradores podem ver essa lista.
    """
    if not request.user.is_admin:
        messages.error(request, 'Acesso negado.')
        return redirect('core:dashboard')

    usuarios = Usuario.objects.all().order_by('first_name')
    return render(request, 'accounts/lista_usuarios.html', {'usuarios': usuarios})


@login_required
def editar_usuario_view(request, pk):
    """Edita os dados de um usuário específico"""
    if not request.user.is_admin:
        messages.error(request, 'Acesso negado.')
        return redirect('core:dashboard')

    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == 'POST':
        form = EdicaoUsuarioForm(request.POST, request.FILES, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuário atualizado com sucesso!')
            return redirect('accounts:lista_usuarios')
    else:
        form = EdicaoUsuarioForm(instance=usuario)

    return render(request, 'accounts/editar_usuario.html', {'form': form, 'usuario': usuario})


@login_required
def excluir_usuario_view(request, pk):
    """Exclui um usuário do sistema"""
    if not request.user.is_admin:
        messages.error(request, 'Acesso negado.')
        return redirect('core:dashboard')

    usuario = get_object_or_404(Usuario, pk=pk)

    # Não pode excluir a si mesmo
    if usuario == request.user:
        messages.error(request, 'Você não pode excluir sua própria conta.')
        return redirect('accounts:lista_usuarios')

    if request.method == 'POST':
        nome = usuario.username
        usuario.delete()
        messages.success(request, f'Usuário {nome} excluído com sucesso!')
        return redirect('accounts:lista_usuarios')

    return render(request, 'accounts/confirmar_exclusao.html', {'usuario': usuario})


@login_required
def perfil_view(request):
    """Tela de perfil do usuário logado - ele pode editar suas próprias informações"""
    if request.method == 'POST':
        form = EdicaoUsuarioForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso!')
            return redirect('accounts:perfil')
    else:
        form = EdicaoUsuarioForm(instance=request.user)

    return render(request, 'accounts/perfil.html', {'form': form})
