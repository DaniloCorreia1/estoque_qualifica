"""
core/management/commands/seed_dados.py
Comando para popular o banco de dados com dados de exemplo.
Execute com: python manage.py seed_dados
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from fornecedores.models import Fornecedor
from produtos.models import Produto, Categoria
from movimentacoes.models import Movimentacao
from decimal import Decimal
import random

Usuario = get_user_model()


class Command(BaseCommand):
    # Texto de ajuda que aparece quando roda: python manage.py help seed_dados
    help = 'Popula o banco de dados com dados de exemplo para demonstração'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('🌱 Iniciando seed de dados...'))

        # ============================================================
        # 1. CRIAR USUÁRIOS
        # ============================================================
        self.stdout.write('👤 Criando usuários...')

        # Admin principal
        admin, criado = Usuario.objects.get_or_create(
            username='admin',
            defaults={
                'first_name': 'Administrador',
                'last_name': 'Sistema',
                'email': 'admin@estoque.com',
                'perfil': 'admin',
                'departamento': 'TI',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if criado:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(f'  ✅ Admin criado: admin / admin123')

        # Funcionário de exemplo
        func, criado = Usuario.objects.get_or_create(
            username='funcionario',
            defaults={
                'first_name': 'João',
                'last_name': 'Silva',
                'email': 'joao@estoque.com',
                'perfil': 'funcionario',
                'departamento': 'Almoxarifado',
                'telefone': '(61) 99999-1111',
            }
        )
        if criado:
            func.set_password('func123')
            func.save()
            self.stdout.write(f'  ✅ Funcionário criado: funcionario / func123')

        # ============================================================
        # 2. CRIAR CATEGORIAS
        # ============================================================
        self.stdout.write('🏷️  Criando categorias...')

        categorias_dados = [
            ('Eletrônicos', '💻', '#3b82f6', 'Computadores, celulares, tablets e acessórios'),
            ('Papelaria', '📝', '#f59e0b', 'Papel, canetas, cadernos e materiais de escritório'),
            ('Limpeza', '🧹', '#22c55e', 'Produtos de higiene e limpeza geral'),
            ('Alimentação', '🍎', '#ef4444', 'Alimentos e bebidas'),
            ('Ferramentas', '🔧', '#8b5cf6', 'Ferramentas manuais e elétricas'),
            ('Roupas', '👕', '#06b6d4', 'Vestuário e acessórios de moda'),
            ('Móveis', '🪑', '#84cc16', 'Móveis e decoração'),
            ('Saúde', '💊', '#f97316', 'Medicamentos e produtos de saúde'),
        ]

        categorias = {}
        for nome, icone, cor, desc in categorias_dados:
            cat, _ = Categoria.objects.get_or_create(
                nome=nome,
                defaults={'icone': icone, 'cor': cor, 'descricao': desc}
            )
            categorias[nome] = cat

        self.stdout.write(f'  ✅ {len(categorias)} categorias criadas')

        # ============================================================
        # 3. CRIAR FORNECEDORES
        # ============================================================
        self.stdout.write('🏢 Criando fornecedores...')

        fornecedores_dados = [
            {
                'nome': 'Tech Distribuidora LTDA',
                'nome_fantasia': 'TechDist',
                'tipo': 'PJ',
                'documento': '12.345.678/0001-90',
                'email': 'contato@techdist.com.br',
                'telefone': '(11) 3000-1234',
                'celular': '(11) 99999-1234',
                'cidade': 'São Paulo', 'estado': 'SP',
                'prazo_entrega': 3,
                'status': 'ativo',
            },
            {
                'nome': 'Papelaria Nacional S.A.',
                'nome_fantasia': 'PapelNac',
                'tipo': 'PJ',
                'documento': '98.765.432/0001-10',
                'email': 'vendas@papelnac.com.br',
                'telefone': '(21) 3100-5678',
                'cidade': 'Rio de Janeiro', 'estado': 'RJ',
                'prazo_entrega': 5,
                'status': 'ativo',
            },
            {
                'nome': 'Clean Produtos de Limpeza',
                'nome_fantasia': 'CleanBR',
                'tipo': 'PJ',
                'documento': '11.222.333/0001-44',
                'email': 'pedidos@cleanbr.com',
                'telefone': '(61) 3200-9999',
                'cidade': 'Brasília', 'estado': 'DF',
                'prazo_entrega': 2,
                'status': 'ativo',
            },
            {
                'nome': 'Alimentos Frescos Distribuidora',
                'nome_fantasia': 'FrescDist',
                'tipo': 'PJ',
                'documento': '55.666.777/0001-88',
                'email': 'comercial@frescdist.com',
                'telefone': '(31) 3300-7777',
                'cidade': 'Belo Horizonte', 'estado': 'MG',
                'prazo_entrega': 1,
                'status': 'ativo',
            },
            {
                'nome': 'Ferramentas Master LTDA',
                'nome_fantasia': 'FerrMaster',
                'tipo': 'PJ',
                'documento': '33.444.555/0001-22',
                'email': 'vendas@ferrmaster.com',
                'telefone': '(41) 3400-6666',
                'cidade': 'Curitiba', 'estado': 'PR',
                'prazo_entrega': 7,
                'status': 'ativo',
            },
        ]

        fornecedores = {}
        for dados in fornecedores_dados:
            f, _ = Fornecedor.objects.get_or_create(
                nome=dados['nome'], defaults=dados
            )
            fornecedores[dados['nome_fantasia']] = f

        self.stdout.write(f'  ✅ {len(fornecedores)} fornecedores criados')

        # ============================================================
        # 4. CRIAR PRODUTOS
        # ============================================================
        self.stdout.write('📦 Criando produtos...')

        produtos_dados = [
            # Eletrônicos
            {'codigo': 'ELET-001', 'nome': 'Notebook Dell Inspiron 15', 'categoria': 'Eletrônicos', 'fornecedor': 'TechDist', 'preco_custo': 2800, 'preco_venda': 3599, 'quantidade': 12, 'estoque_minimo': 3, 'estoque_maximo': 30, 'unidade': 'un', 'localizacao': 'Prateleira A1'},
            {'codigo': 'ELET-002', 'nome': 'Mouse Sem Fio Logitech', 'categoria': 'Eletrônicos', 'fornecedor': 'TechDist', 'preco_custo': 45, 'preco_venda': 89.90, 'quantidade': 25, 'estoque_minimo': 10, 'estoque_maximo': 100, 'unidade': 'un', 'localizacao': 'Prateleira A2'},
            {'codigo': 'ELET-003', 'nome': 'Teclado Mecânico RGB', 'categoria': 'Eletrônicos', 'fornecedor': 'TechDist', 'preco_custo': 120, 'preco_venda': 249, 'quantidade': 8, 'estoque_minimo': 5, 'estoque_maximo': 50, 'unidade': 'un', 'localizacao': 'Prateleira A3'},
            {'codigo': 'ELET-004', 'nome': 'Monitor 24" Full HD', 'categoria': 'Eletrônicos', 'fornecedor': 'TechDist', 'preco_custo': 680, 'preco_venda': 999, 'quantidade': 2, 'estoque_minimo': 3, 'estoque_maximo': 20, 'unidade': 'un', 'localizacao': 'Prateleira A4'},
            {'codigo': 'ELET-005', 'nome': 'Cabo HDMI 2m', 'categoria': 'Eletrônicos', 'fornecedor': 'TechDist', 'preco_custo': 12, 'preco_venda': 29.90, 'quantidade': 0, 'estoque_minimo': 15, 'estoque_maximo': 200, 'unidade': 'un', 'localizacao': 'Prateleira A5'},
            # Papelaria
            {'codigo': 'PAP-001', 'nome': 'Papel A4 500 folhas', 'categoria': 'Papelaria', 'fornecedor': 'PapelNac', 'preco_custo': 18, 'preco_venda': 32.90, 'quantidade': 40, 'estoque_minimo': 10, 'estoque_maximo': 200, 'unidade': 'cx', 'localizacao': 'Prateleira B1'},
            {'codigo': 'PAP-002', 'nome': 'Caneta Esferográfica (cx 50un)', 'categoria': 'Papelaria', 'fornecedor': 'PapelNac', 'preco_custo': 22, 'preco_venda': 45, 'quantidade': 15, 'estoque_minimo': 5, 'estoque_maximo': 100, 'unidade': 'cx', 'localizacao': 'Prateleira B2'},
            {'codigo': 'PAP-003', 'nome': 'Caderno universitário 200f', 'categoria': 'Papelaria', 'fornecedor': 'PapelNac', 'preco_custo': 8.50, 'preco_venda': 19.90, 'quantidade': 3, 'estoque_minimo': 10, 'estoque_maximo': 150, 'unidade': 'un', 'localizacao': 'Prateleira B3'},
            {'codigo': 'PAP-004', 'nome': 'Grampeador de Mesa', 'categoria': 'Papelaria', 'fornecedor': 'PapelNac', 'preco_custo': 15, 'preco_venda': 34.90, 'quantidade': 7, 'estoque_minimo': 5, 'estoque_maximo': 50, 'unidade': 'un', 'localizacao': 'Prateleira B4'},
            # Limpeza
            {'codigo': 'LIM-001', 'nome': 'Álcool 70% 1 litro', 'categoria': 'Limpeza', 'fornecedor': 'CleanBR', 'preco_custo': 5.50, 'preco_venda': 12.90, 'quantidade': 60, 'estoque_minimo': 20, 'estoque_maximo': 300, 'unidade': 'un', 'localizacao': 'Prateleira C1'},
            {'codigo': 'LIM-002', 'nome': 'Desinfetante Pinho 2L', 'categoria': 'Limpeza', 'fornecedor': 'CleanBR', 'preco_custo': 7, 'preco_venda': 16.90, 'quantidade': 4, 'estoque_minimo': 10, 'estoque_maximo': 100, 'unidade': 'un', 'localizacao': 'Prateleira C2'},
            {'codigo': 'LIM-003', 'nome': 'Papel Toalha (fardo 6un)', 'categoria': 'Limpeza', 'fornecedor': 'CleanBR', 'preco_custo': 16, 'preco_venda': 32.90, 'quantidade': 25, 'estoque_minimo': 8, 'estoque_maximo': 120, 'unidade': 'pc', 'localizacao': 'Prateleira C3'},
            # Ferramentas
            {'codigo': 'FER-001', 'nome': 'Chave de Fenda Philips', 'categoria': 'Ferramentas', 'fornecedor': 'FerrMaster', 'preco_custo': 8, 'preco_venda': 19.90, 'quantidade': 18, 'estoque_minimo': 5, 'estoque_maximo': 50, 'unidade': 'un', 'localizacao': 'Prateleira D1'},
            {'codigo': 'FER-002', 'nome': 'Alicate Universal 8"', 'categoria': 'Ferramentas', 'fornecedor': 'FerrMaster', 'preco_custo': 25, 'preco_venda': 54.90, 'quantidade': 9, 'estoque_minimo': 3, 'estoque_maximo': 30, 'unidade': 'un', 'localizacao': 'Prateleira D2'},
            {'codigo': 'FER-003', 'nome': 'Fita Isolante (rolo)', 'categoria': 'Ferramentas', 'fornecedor': 'FerrMaster', 'preco_custo': 3.50, 'preco_venda': 8.90, 'quantidade': 0, 'estoque_minimo': 10, 'estoque_maximo': 100, 'unidade': 'un', 'localizacao': 'Prateleira D3'},
        ]

        produtos_criados = {}
        for dados in produtos_dados:
            cat = categorias.get(dados.pop('categoria'))
            forn_key = dados.pop('fornecedor')
            forn = fornecedores.get(forn_key)
            p, _ = Produto.objects.get_or_create(
                codigo=dados['codigo'],
                defaults={
                    **dados,
                    'categoria': cat,
                    'fornecedor': forn,
                    'preco_custo': Decimal(str(dados['preco_custo'])),
                    'preco_venda': Decimal(str(dados['preco_venda'])),
                    'quantidade': Decimal(str(dados['quantidade'])),
                    'estoque_minimo': Decimal(str(dados['estoque_minimo'])),
                    'estoque_maximo': Decimal(str(dados['estoque_maximo'])),
                    'status': 'ativo',
                }
            )
            produtos_criados[dados['codigo']] = p

        self.stdout.write(f'  ✅ {len(produtos_criados)} produtos criados')

        # ============================================================
        # 5. CRIAR MOVIMENTAÇÕES DE EXEMPLO
        # ============================================================
        self.stdout.write('📊 Criando movimentações...')

        from django.utils import timezone
        from datetime import timedelta

        movs_criados = 0
        for i, (cod, produto) in enumerate(list(produtos_criados.items())[:8]):
            # Entrada inicial (compra)
            if not Movimentacao.objects.filter(produto=produto, tipo='entrada').exists():
                qtd_entrada = random.randint(20, 50)
                # Salvar diretamente sem chamar o save() que atualiza estoque
                # (pois o estoque já foi setado no produto)
                Movimentacao.objects.create(
                    produto=produto,
                    tipo='entrada',
                    motivo='compra',
                    quantidade=Decimal(str(qtd_entrada)),
                    preco_unitario=produto.preco_custo,
                    estoque_anterior=Decimal('0'),
                    estoque_posterior=produto.quantidade,
                    numero_documento=f'NF-{1000+i}',
                    usuario=admin,
                    observacoes='Compra inicial de estoque'
                )
                movs_criados += 1

        self.stdout.write(f'  ✅ {movs_criados} movimentações criadas')

        # ============================================================
        # RESUMO FINAL
        # ============================================================
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('✅ SEED CONCLUÍDO COM SUCESSO!'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(f'  👤 Usuários: {Usuario.objects.count()}')
        self.stdout.write(f'  🏷️  Categorias: {Categoria.objects.count()}')
        self.stdout.write(f'  🏢 Fornecedores: {Fornecedor.objects.count()}')
        self.stdout.write(f'  📦 Produtos: {Produto.objects.count()}')
        self.stdout.write(f'  📊 Movimentações: {Movimentacao.objects.count()}')
        self.stdout.write('')
        self.stdout.write('  🔑 Login de ADMIN: admin / admin123')
        self.stdout.write('  🔑 Login de Funcionário: funcionario / func123')
        self.stdout.write(self.style.SUCCESS('=' * 50))
