"""
core/views.py - Dashboard principal com análise de IA
Esta é a tela mais importante do sistema - o painel de controle.
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Sum, Count, F, Q
from django.utils import timezone
from datetime import timedelta
import json
import os

from produtos.models import Produto, Categoria
from movimentacoes.models import Movimentacao
from fornecedores.models import Fornecedor
from accounts.models import Usuario


@login_required
def dashboard(request):
    """
    Dashboard principal com indicadores, gráficos e análise de IA.
    Reúne dados de todos os apps para mostrar uma visão geral do estoque.
    """
    hoje = timezone.now()
    inicio_mes = hoje.replace(day=1, hour=0, minute=0, second=0)
    inicio_semana = hoje - timedelta(days=7)

    # ============================================================
    # CARDS DE INDICADORES (os 4 números grandes do topo)
    # ============================================================
    total_produtos = Produto.objects.filter(status='ativo').count()
    total_fornecedores = Fornecedor.objects.filter(status='ativo').count()

    # Produtos com estoque abaixo do mínimo
    produtos_alerta = Produto.objects.filter(
        status='ativo',
        quantidade__lte=F('estoque_minimo')
    ).count()

    # Movimentações do mês atual
    movimentacoes_mes = Movimentacao.objects.filter(
        criado_em__gte=inicio_mes
    ).count()

    # Valor total do estoque
    produtos_ativos = Produto.objects.filter(status='ativo')
    valor_estoque = sum(p.valor_estoque for p in produtos_ativos)

    # ============================================================
    # PRODUTOS CRÍTICOS (estoque baixo ou zerado)
    # ============================================================
    produtos_criticos = Produto.objects.filter(
        status='ativo',
        quantidade__lte=F('estoque_minimo')
    ).select_related('categoria', 'fornecedor').order_by('quantidade')[:10]

    # ============================================================
    # ÚLTIMAS MOVIMENTAÇÕES
    # ============================================================
    ultimas_movimentacoes = Movimentacao.objects.select_related(
        'produto', 'usuario'
    ).order_by('-criado_em')[:8]

    # ============================================================
    # DADOS PARA O GRÁFICO DE LINHA (movimentações da semana)
    # ============================================================
    dias_labels = []
    entradas_semana = []
    saidas_semana = []

    for i in range(6, -1, -1):
        dia = (hoje - timedelta(days=i)).date()
        dias_labels.append(dia.strftime('%d/%m'))

        entrada = Movimentacao.objects.filter(
            tipo='entrada', criado_em__date=dia
        ).aggregate(total=Sum('quantidade'))['total'] or 0
        saida = Movimentacao.objects.filter(
            tipo='saida', criado_em__date=dia
        ).aggregate(total=Sum('quantidade'))['total'] or 0

        entradas_semana.append(float(entrada))
        saidas_semana.append(float(saida))

    # ============================================================
    # DADOS PARA GRÁFICO DE ROSCA (distribuição por categoria)
    # ============================================================
    categorias = Categoria.objects.annotate(
        qtd=Count('produto', filter=Q(produto__status='ativo'))
    ).filter(qtd__gt=0)[:6]
    cat_labels = [c.nome for c in categorias]
    cat_qtd = [c.qtd for c in categorias]

    context = {
        # Cards
        'total_produtos': total_produtos,
        'total_fornecedores': total_fornecedores,
        'produtos_alerta': produtos_alerta,
        'movimentacoes_mes': movimentacoes_mes,
        'valor_estoque': valor_estoque,
        # Listas
        'produtos_criticos': produtos_criticos,
        'ultimas_movimentacoes': ultimas_movimentacoes,
        # JSON para gráficos
        'dias_labels_json': json.dumps(dias_labels),
        'entradas_semana_json': json.dumps(entradas_semana),
        'saidas_semana_json': json.dumps(saidas_semana),
        'cat_labels_json': json.dumps(cat_labels),
        'cat_qtd_json': json.dumps(cat_qtd),
        # Info adicional
        'total_usuarios': Usuario.objects.filter(is_active=True).count(),
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def ia_analise(request):
    """
    Endpoint AJAX que usa a API da OpenAI para analisar o estoque
    e retornar insights inteligentes. Chamado pelo JavaScript do dashboard.
    """
    # Só aceita requisições POST (segurança)
    if request.method != 'POST':
        return JsonResponse({'erro': 'Método não permitido'}, status=405)

    # Coleta dados do estoque para enviar para a IA
    # Converte Decimal para float para evitar erro de serialização JSON
    produtos_criticos = [
        {
            'nome': p['nome'],
            'quantidade': float(p['quantidade']),
            'estoque_minimo': float(p['estoque_minimo']),
            'unidade': p['unidade'],
        }
        for p in Produto.objects.filter(
            status='ativo',
            quantidade__lte=F('estoque_minimo')
        ).values('nome', 'quantidade', 'estoque_minimo', 'unidade')[:15]
    ]

    produtos_zerados = Produto.objects.filter(
        status='ativo', quantidade__lte=0
    ).count()

    # Movimentações da última semana
    semana_passada = timezone.now() - timedelta(days=7)
    mov_semana = Movimentacao.objects.filter(criado_em__gte=semana_passada)
    total_entradas = mov_semana.filter(tipo='entrada').aggregate(
        t=Sum('quantidade'))['t'] or 0
    total_saidas = mov_semana.filter(tipo='saida').aggregate(
        t=Sum('quantidade'))['t'] or 0

    # Produto mais vendido/saído na semana
    top_saida = mov_semana.filter(tipo='saida').values(
        'produto__nome'
    ).annotate(total=Sum('quantidade')).order_by('-total').first()

    # Monta o contexto para a IA
    contexto_ia = {
        'total_produtos_ativos': Produto.objects.filter(status='ativo').count(),
        'produtos_abaixo_minimo': len(produtos_criticos),
        'produtos_zerados': produtos_zerados,
        'lista_criticos': produtos_criticos[:5],
        'entradas_semana': float(total_entradas),
        'saidas_semana': float(total_saidas),
        'produto_mais_saido': top_saida['produto__nome'] if top_saida else 'N/A',
        'total_fornecedores': Fornecedor.objects.filter(status='ativo').count(),
    }

    # Prepara o prompt para a IA
    prompt = f"""Você é um assistente especialista em gestão de estoque para pequenas e médias empresas.
Analise os seguintes dados do sistema de estoque e forneça insights valiosos em português:

DADOS DO ESTOQUE:
- Total de produtos ativos: {contexto_ia['total_produtos_ativos']}
- Produtos abaixo do estoque mínimo: {contexto_ia['produtos_abaixo_minimo']}
- Produtos zerados (sem estoque): {contexto_ia['produtos_zerados']}
- Total de fornecedores ativos: {contexto_ia['total_fornecedores']}

MOVIMENTAÇÕES DA ÚLTIMA SEMANA:
- Total de entradas: {contexto_ia['entradas_semana']} unidades
- Total de saídas: {contexto_ia['saidas_semana']} unidades
- Produto com mais saídas: {contexto_ia['produto_mais_saido']}

PRODUTOS CRÍTICOS (abaixo do mínimo):
{json.dumps(contexto_ia['lista_criticos'], ensure_ascii=False, indent=2)}

Por favor, forneça:
1. 🔴 ALERTAS URGENTES: Situações que precisam de atenção imediata
2. 📊 ANÁLISE GERAL: Situação atual do estoque em poucas palavras
3. 💡 RECOMENDAÇÕES: 3 ações práticas para melhorar a gestão
4. 📈 TENDÊNCIA: Com base nas movimentações, o que você observa?

Seja direto, prático e use linguagem simples. Limite sua resposta a 400 palavras."""

    try:
        from openai import OpenAI

        api_key = os.getenv('OPENAI_API_KEY', '')
        if not api_key:
            # Se não tiver API key, retorna uma análise local (modo offline)
            return JsonResponse({
                'analise': gerar_analise_local(contexto_ia),
                'modo': 'local'
            })

        client = OpenAI(api_key=api_key)

        # Faz a chamada para a API da OpenAI
        resposta = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um consultor especialista em gestão de estoque e supply chain, focado em pequenas e médias empresas brasileiras. Responda sempre em português, de forma clara e prática."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=600,
            temperature=0.7
        )

        analise = resposta.choices[0].message.content
        return JsonResponse({'analise': analise, 'modo': 'openai'})

    except Exception as e:
        # Se der erro na API, usa análise local
        return JsonResponse({
            'analise': gerar_analise_local(contexto_ia),
            'modo': 'local',
            'aviso': f'IA offline: {str(e)}'
        })


def gerar_analise_local(dados):
    """
    Gera uma análise básica sem usar a API da OpenAI.
    Usada como fallback quando não há chave de API configurada.
    """
    linhas = []

    # Alertas urgentes
    if dados['produtos_zerados'] > 0:
        linhas.append(f"🔴 **ALERTA URGENTE:** {dados['produtos_zerados']} produto(s) estão completamente sem estoque! Providencie reposição imediatamente.")

    if dados['produtos_abaixo_minimo'] > 0:
        linhas.append(f"⚠️ **ATENÇÃO:** {dados['produtos_abaixo_minimo']} produto(s) abaixo do estoque mínimo.")
        if dados['lista_criticos']:
            nomes = ', '.join([p['nome'] for p in dados['lista_criticos'][:3]])
            linhas.append(f"   Produtos críticos: {nomes}")

    # Análise de movimentações
    if dados['entradas_semana'] > 0 or dados['saidas_semana'] > 0:
        linhas.append(f"\n📊 **SEMANA:** {dados['entradas_semana']:.0f} unidades entraram e {dados['saidas_semana']:.0f} saíram do estoque.")

    if dados['produto_mais_saido'] != 'N/A':
        linhas.append(f"🏆 Produto com mais movimento: **{dados['produto_mais_saido']}**")

    # Recomendações
    linhas.append("\n💡 **RECOMENDAÇÕES:**")
    if dados['produtos_abaixo_minimo'] > 0:
        linhas.append("• Entre em contato com fornecedores para repor produtos críticos")
    if dados['produtos_zerados'] > 0:
        linhas.append("• Priorize compra emergencial dos produtos zerados")
    linhas.append("• Realize uma contagem física mensal para confirmar os dados do sistema")
    linhas.append("• Configure alertas automáticos de estoque mínimo para todos os produtos")

    if not linhas:
        linhas.append("✅ **Estoque saudável!** Todos os produtos estão com níveis adequados. Continue monitorando diariamente.")

    return "\n".join(linhas)


def index(request):
    """Redireciona a raiz para login ou dashboard"""
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return redirect('accounts:login')