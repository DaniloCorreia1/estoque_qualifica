"""
produtos/views.py - Views do CRUD de produtos
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Produto, Categoria
from .forms import ProdutoForm, CategoriaForm


@login_required
def lista_produtos(request):
    """Lista todos os produtos com busca e filtros"""
    busca = request.GET.get('busca', '')
    categoria_filtro = request.GET.get('categoria', '')
    status_filtro = request.GET.get('status', '')
    estoque_filtro = request.GET.get('estoque', '')

    produtos = Produto.objects.select_related('categoria', 'fornecedor').all()

    if busca:
        produtos = produtos.filter(
            Q(nome__icontains=busca) |
            Q(codigo__icontains=busca) |
            Q(codigo_barras__icontains=busca) |
            Q(descricao__icontains=busca)
        )

    if categoria_filtro:
        produtos = produtos.filter(categoria_id=categoria_filtro)

    if status_filtro:
        produtos = produtos.filter(status=status_filtro)

    # Filtro especial para estoque baixo/zerado
    if estoque_filtro == 'baixo':
        from django.db.models import F
        produtos = produtos.filter(quantidade__lte=F('estoque_minimo'))
    elif estoque_filtro == 'zerado':
        produtos = produtos.filter(quantidade__lte=0)

    categorias = Categoria.objects.all()

    context = {
        'produtos': produtos,
        'categorias': categorias,
        'busca': busca,
        'categoria_filtro': categoria_filtro,
        'status_filtro': status_filtro,
        'estoque_filtro': estoque_filtro,
        'total': produtos.count(),
    }
    return render(request, 'produtos/lista.html', context)


@login_required
def detalhe_produto(request, pk):
    """Mostra detalhes de um produto e seu histórico de movimentações"""
    produto = get_object_or_404(Produto, pk=pk)
    # Pega as últimas 20 movimentações deste produto
    movimentacoes = produto.movimentacao_set.select_related('usuario').order_by('-criado_em')[:20]
    return render(request, 'produtos/detalhe.html', {
        'produto': produto,
        'movimentacoes': movimentacoes
    })


@login_required
def criar_produto(request):
    """Cria um novo produto no estoque"""
    if not request.user.is_admin:
        messages.error(request, 'Apenas administradores podem cadastrar produtos.')
        return redirect('produtos:lista')

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            produto = form.save()
            messages.success(request, f'Produto "{produto.nome}" cadastrado com sucesso!')
            return redirect('produtos:lista')
        else:
            messages.error(request, 'Erro ao cadastrar produto. Verifique os campos.')
    else:
        form = ProdutoForm()

    categorias = Categoria.objects.all()
    return render(request, 'produtos/form.html', {
        'form': form,
        'acao': 'Cadastrar',
        'categorias': categorias
    })


@login_required
def editar_produto(request, pk):
    """Edita um produto existente"""
    if not request.user.is_admin:
        messages.error(request, 'Apenas administradores podem editar produtos.')
        return redirect('produtos:lista')

    produto = get_object_or_404(Produto, pk=pk)

    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, f'Produto "{produto.nome}" atualizado com sucesso!')
            return redirect('produtos:lista')
    else:
        form = ProdutoForm(instance=produto)

    return render(request, 'produtos/form.html', {
        'form': form,
        'acao': 'Editar',
        'produto': produto
    })


@login_required
def excluir_produto(request, pk):
    """Exclui um produto"""
    if not request.user.is_admin:
        messages.error(request, 'Apenas administradores podem excluir produtos.')
        return redirect('produtos:lista')

    produto = get_object_or_404(Produto, pk=pk)

    if request.method == 'POST':
        if produto.movimentacao_set.exists():
            messages.error(request, 'Não é possível excluir. Este produto possui movimentações registradas.')
            return redirect('produtos:lista')
        nome = produto.nome
        produto.delete()
        messages.success(request, f'Produto "{nome}" excluído com sucesso!')
        return redirect('produtos:lista')

    return render(request, 'produtos/confirmar_exclusao.html', {'produto': produto})


@login_required
def lista_categorias(request):
    """Lista e gerencia categorias de produtos"""
    categorias = Categoria.objects.all()
    form = CategoriaForm()

    if request.method == 'POST':
        if not request.user.is_admin:
            messages.error(request, 'Acesso negado.')
            return redirect('produtos:lista')
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria criada com sucesso!')
            return redirect('produtos:categorias')

    return render(request, 'produtos/categorias.html', {
        'categorias': categorias,
        'form': form
    })


@login_required
def excluir_categoria(request, pk):
    """Exclui uma categoria"""
    if not request.user.is_admin:
        messages.error(request, 'Acesso negado.')
        return redirect('produtos:categorias')

    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        if categoria.produto_set.exists():
            messages.error(request, 'Não é possível excluir. Existem produtos nesta categoria.')
        else:
            categoria.delete()
            messages.success(request, 'Categoria excluída.')
        return redirect('produtos:categorias')

    return render(request, 'produtos/confirmar_exclusao_categoria.html', {'categoria': categoria})
