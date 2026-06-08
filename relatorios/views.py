"""
relatorios/views.py - Relatórios completos do sistema
"""
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F, Q
from django.utils import timezone
from datetime import timedelta, date
import json
from movimentacoes.models import Movimentacao
from produtos.models import Produto, Categoria
from fornecedores.models import Fornecedor


@login_required
def relatorios_home(request):
    """
    Página principal de relatórios.
    Gera dados para gráficos semanais e mensais.
    """
    hoje = timezone.now()
    periodo = request.GET.get('periodo', 'mensal')

    # Define o período de análise
    if periodo == 'semanal':
        data_inicio = hoje - timedelta(days=7)
        titulo_periodo = 'Últimos 7 dias'
    elif periodo == 'quinzenal':
        data_inicio = hoje - timedelta(days=15)
        titulo_periodo = 'Últimos 15 dias'
    else:  # mensal (padrão)
        data_inicio = hoje - timedelta(days=30)
        titulo_periodo = 'Últimos 30 dias'

    # ============================================================
    # DADOS DE MOVIMENTAÇÕES
    # ============================================================
    movimentacoes_periodo = Movimentacao.objects.filter(
        criado_em__gte=data_inicio
    ).select_related('produto', 'usuario')

    # Total de entradas e saídas
    total_entradas_qtd = movimentacoes_periodo.filter(
        tipo='entrada').aggregate(total=Sum('quantidade'))['total'] or 0
    total_saidas_qtd = movimentacoes_periodo.filter(
        tipo='saida').aggregate(total=Sum('quantidade'))['total'] or 0

    # Valor financeiro das movimentações
    total_entradas_valor = movimentacoes_periodo.filter(tipo='entrada').aggregate(
        total=Sum(F('quantidade') * F('preco_unitario')))['total'] or 0
    total_saidas_valor = movimentacoes_periodo.filter(tipo='saida').aggregate(
        total=Sum(F('quantidade') * F('preco_unitario')))['total'] or 0

    # ============================================================
    # DADOS DO ESTOQUE
    # ============================================================
    produtos_todos = Produto.objects.filter(status='ativo')
    total_produtos = produtos_todos.count()

    # Produtos abaixo do mínimo (críticos)
    produtos_criticos = produtos_todos.filter(
        quantidade__lte=F('estoque_minimo')
    ).order_by('quantidade')

    # Produtos zerados
    produtos_zerados = produtos_todos.filter(quantidade__lte=0)

    # Valor total do estoque
    valor_total_estoque = sum(p.valor_estoque for p in produtos_todos)

    # ============================================================
    # GRÁFICO: Movimentações por dia (últimos N dias)
    # ============================================================
    dias_labels = []
    dados_entradas = []
    dados_saidas = []

    num_dias = 7 if periodo == 'semanal' else (15 if periodo == 'quinzenal' else 30)
    for i in range(num_dias - 1, -1, -1):
        dia = (hoje - timedelta(days=i)).date()
        dias_labels.append(dia.strftime('%d/%m'))

        entrada_dia = movimentacoes_periodo.filter(
            tipo='entrada',
            criado_em__date=dia
        ).aggregate(total=Sum('quantidade'))['total'] or 0

        saida_dia = movimentacoes_periodo.filter(
            tipo='saida',
            criado_em__date=dia
        ).aggregate(total=Sum('quantidade'))['total'] or 0

        dados_entradas.append(float(entrada_dia))
        dados_saidas.append(float(saida_dia))

    # ============================================================
    # GRÁFICO: Produtos por categoria
    # ============================================================
    categorias_dados = Categoria.objects.annotate(
        total_produtos=Count('produto')
    ).filter(total_produtos__gt=0)

    cat_labels = [c.nome for c in categorias_dados]
    cat_valores = [c.total_produtos for c in categorias_dados]

    # ============================================================
    # TOP 10 produtos mais movimentados
    # ============================================================
    top_produtos = Movimentacao.objects.filter(
        criado_em__gte=data_inicio
    ).values(
        'produto__nome', 'produto__codigo'
    ).annotate(
        total_mov=Sum('quantidade')
    ).order_by('-total_mov')[:10]

    # ============================================================
    # MOVIMENTAÇÕES RECENTES (tabela detalhada)
    # ============================================================
    movimentacoes_recentes = movimentacoes_periodo.order_by('-criado_em')[:50]

    context = {
        'periodo': periodo,
        'titulo_periodo': titulo_periodo,
        'total_entradas_qtd': total_entradas_qtd,
        'total_saidas_qtd': total_saidas_qtd,
        'total_entradas_valor': total_entradas_valor,
        'total_saidas_valor': total_saidas_valor,
        'total_produtos': total_produtos,
        'produtos_criticos': produtos_criticos,
        'produtos_zerados_count': produtos_zerados.count(),
        'valor_total_estoque': valor_total_estoque,
        'movimentacoes_recentes': movimentacoes_recentes,
        'top_produtos': top_produtos,
        # Dados JSON para os gráficos JavaScript
        'dias_labels_json': json.dumps(dias_labels),
        'dados_entradas_json': json.dumps(dados_entradas),
        'dados_saidas_json': json.dumps(dados_saidas),
        'cat_labels_json': json.dumps(cat_labels),
        'cat_valores_json': json.dumps(cat_valores),
        'total_fornecedores': Fornecedor.objects.filter(status='ativo').count(),
    }

    return render(request, 'relatorios/relatorios.html', context)
