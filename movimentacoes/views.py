"""
movimentacoes/views.py - Views de movimentação de estoque
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.utils import timezone
from datetime import timedelta
from .models import Movimentacao
from .forms import EntradaForm, SaidaForm, AjusteForm
from produtos.models import Produto


@login_required
def lista_movimentacoes(request):
    """Lista todas as movimentações com filtros"""
    busca = request.GET.get('busca', '')
    tipo_filtro = request.GET.get('tipo', '')
    periodo = request.GET.get('periodo', '30')  # últimos 30 dias por padrão

    # Define o período de busca
    dias = int(periodo) if periodo.isdigit() else 30
    data_inicio = timezone.now() - timedelta(days=dias)

    movimentacoes = Movimentacao.objects.select_related(
        'produto', 'usuario'
    ).filter(criado_em__gte=data_inicio)

    if busca:
        movimentacoes = movimentacoes.filter(
            Q(produto__nome__icontains=busca) |
            Q(produto__codigo__icontains=busca) |
            Q(numero_documento__icontains=busca) |
            Q(observacoes__icontains=busca)
        )

    if tipo_filtro:
        movimentacoes = movimentacoes.filter(tipo=tipo_filtro)

    # Totalizadores
    total_entradas = movimentacoes.filter(tipo='entrada').aggregate(
        total=Sum('quantidade'))['total'] or 0
    total_saidas = movimentacoes.filter(tipo='saida').aggregate(
        total=Sum('quantidade'))['total'] or 0

    context = {
        'movimentacoes': movimentacoes.order_by('-criado_em'),
        'busca': busca,
        'tipo_filtro': tipo_filtro,
        'periodo': periodo,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'total_registros': movimentacoes.count(),
    }
    return render(request, 'movimentacoes/lista.html', context)


@login_required
def registrar_entrada(request):
    """Registra uma entrada de produtos no estoque (ex: compra de mercadorias)"""
    if request.method == 'POST':
        form = EntradaForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False)
            movimentacao.tipo = 'entrada'
            movimentacao.usuario = request.user  # Registra quem fez a movimentação
            movimentacao.save()
            messages.success(
                request,
                f'Entrada registrada: {movimentacao.quantidade} {movimentacao.produto.get_unidade_display()} de "{movimentacao.produto.nome}"'
            )
            return redirect('movimentacoes:lista')
        else:
            messages.error(request, 'Erro ao registrar entrada. Verifique os campos.')
    else:
        # Pré-seleciona produto se passado na URL (?produto=ID)
        produto_id = request.GET.get('produto')
        initial = {}
        if produto_id:
            initial['produto'] = produto_id
        form = EntradaForm(initial=initial)

    return render(request, 'movimentacoes/entrada.html', {'form': form})


@login_required
def registrar_saida(request):
    """Registra uma saída de produtos do estoque (ex: venda, uso interno)"""
    if request.method == 'POST':
        form = SaidaForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False)
            movimentacao.tipo = 'saida'
            movimentacao.usuario = request.user

            # Verifica se tem estoque suficiente
            produto = movimentacao.produto
            if movimentacao.quantidade > produto.quantidade:
                messages.error(
                    request,
                    f'Estoque insuficiente! Disponível: {produto.quantidade} {produto.get_unidade_display()}'
                )
                return render(request, 'movimentacoes/saida.html', {'form': form})

            movimentacao.save()
            messages.success(
                request,
                f'Saída registrada: {movimentacao.quantidade} {movimentacao.produto.get_unidade_display()} de "{movimentacao.produto.nome}"'
            )
            return redirect('movimentacoes:lista')
        else:
            messages.error(request, 'Erro ao registrar saída. Verifique os campos.')
    else:
        produto_id = request.GET.get('produto')
        initial = {}
        if produto_id:
            initial['produto'] = produto_id
        form = SaidaForm(initial=initial)

    return render(request, 'movimentacoes/saida.html', {'form': form})


@login_required
def registrar_ajuste(request):
    """Ajuste de inventário - corrige a quantidade quando há diferença física"""
    if not request.user.is_admin:
        messages.error(request, 'Apenas administradores podem fazer ajustes de inventário.')
        return redirect('movimentacoes:lista')

    if request.method == 'POST':
        form = AjusteForm(request.POST)
        if form.is_valid():
            movimentacao = form.save(commit=False)
            movimentacao.tipo = 'ajuste'
            movimentacao.usuario = request.user
            movimentacao.save()
            messages.success(request, f'Ajuste realizado para "{movimentacao.produto.nome}"!')
            return redirect('movimentacoes:lista')
    else:
        form = AjusteForm()

    return render(request, 'movimentacoes/ajuste.html', {'form': form})


@login_required
def detalhe_movimentacao(request, pk):
    """Mostra os detalhes de uma movimentação específica"""
    movimentacao = get_object_or_404(Movimentacao, pk=pk)
    return render(request, 'movimentacoes/detalhe.html', {'movimentacao': movimentacao})
