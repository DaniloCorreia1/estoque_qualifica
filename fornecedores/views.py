"""
fornecedores/views.py - Views do CRUD de fornecedores
CRUD = Create (criar), Read (ler), Update (atualizar), Delete (excluir)
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q  # Para fazer buscas com múltiplos filtros
from .models import Fornecedor
from .forms import FornecedorForm


@login_required
def lista_fornecedores(request):
    """
    Lista todos os fornecedores com opção de busca.
    O @login_required garante que só usuários logados acessem essa página.
    """
    # Pega o termo de busca digitado pelo usuário (se houver)
    busca = request.GET.get('busca', '')

    # Começa com todos os fornecedores
    fornecedores = Fornecedor.objects.all()

    # Se o usuário digitou algo na busca, filtra os resultados
    if busca:
        fornecedores = fornecedores.filter(
            Q(nome__icontains=busca) |           # Busca no nome
            Q(nome_fantasia__icontains=busca) |   # Busca no nome fantasia
            Q(documento__icontains=busca) |        # Busca no CNPJ/CPF
            Q(cidade__icontains=busca)             # Busca na cidade
        )

    # Filtro por status
    status_filtro = request.GET.get('status', '')
    if status_filtro:
        fornecedores = fornecedores.filter(status=status_filtro)

    # Envia os dados para o template HTML
    context = {
        'fornecedores': fornecedores,
        'busca': busca,
        'status_filtro': status_filtro,
        'total': fornecedores.count(),
    }
    return render(request, 'fornecedores/lista.html', context)


@login_required
def detalhe_fornecedor(request, pk):
    """Mostra os detalhes de um fornecedor específico"""
    # get_object_or_404 busca o fornecedor ou retorna erro 404 se não existir
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    # Pega os produtos desse fornecedor
    produtos = fornecedor.produto_set.all()
    return render(request, 'fornecedores/detalhe.html', {
        'fornecedor': fornecedor,
        'produtos': produtos
    })


@login_required
def criar_fornecedor(request):
    """
    Cria um novo fornecedor.
    GET: mostra o formulário em branco
    POST: processa o formulário e salva no banco
    """
    # Apenas administradores podem criar fornecedores
    if not request.user.is_admin:
        messages.error(request, 'Apenas administradores podem cadastrar fornecedores.')
        return redirect('fornecedores:lista')

    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            fornecedor = form.save()
            messages.success(request, f'Fornecedor "{fornecedor.nome}" cadastrado com sucesso!')
            return redirect('fornecedores:lista')
        else:
            messages.error(request, 'Erro ao cadastrar. Verifique os campos.')
    else:
        form = FornecedorForm()  # Formulário vazio

    return render(request, 'fornecedores/form.html', {'form': form, 'acao': 'Cadastrar'})


@login_required
def editar_fornecedor(request, pk):
    """Edita os dados de um fornecedor existente"""
    if not request.user.is_admin:
        messages.error(request, 'Apenas administradores podem editar fornecedores.')
        return redirect('fornecedores:lista')

    fornecedor = get_object_or_404(Fornecedor, pk=pk)

    if request.method == 'POST':
        # instance=fornecedor diz ao Django para atualizar o registro existente
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            messages.success(request, f'Fornecedor "{fornecedor.nome}" atualizado!')
            return redirect('fornecedores:lista')
    else:
        form = FornecedorForm(instance=fornecedor)  # Pré-preenche o formulário

    return render(request, 'fornecedores/form.html', {
        'form': form,
        'acao': 'Editar',
        'fornecedor': fornecedor
    })


@login_required
def excluir_fornecedor(request, pk):
    """Exclui um fornecedor"""
    if not request.user.is_admin:
        messages.error(request, 'Apenas administradores podem excluir fornecedores.')
        return redirect('fornecedores:lista')

    fornecedor = get_object_or_404(Fornecedor, pk=pk)

    if request.method == 'POST':
        # Verifica se tem produtos vinculados
        if fornecedor.produto_set.exists():
            messages.error(request, 'Não é possível excluir. Este fornecedor possui produtos cadastrados.')
            return redirect('fornecedores:lista')
        nome = fornecedor.nome
        fornecedor.delete()
        messages.success(request, f'Fornecedor "{nome}" excluído com sucesso!')
        return redirect('fornecedores:lista')

    return render(request, 'fornecedores/confirmar_exclusao.html', {'fornecedor': fornecedor})
