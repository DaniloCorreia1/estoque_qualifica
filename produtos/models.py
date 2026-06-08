"""
produtos/models.py - Modelo de Produto
Define como os produtos são armazenados no banco de dados
"""
from django.db import models
from fornecedores.models import Fornecedor


class Categoria(models.Model):
    """
    Categoria do produto. Exemplos: Eletrônicos, Papelaria, Alimentos, etc.
    Permite organizar os produtos por tipo.
    """
    nome = models.CharField(max_length=100, verbose_name='Nome')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição')
    icone = models.CharField(max_length=50, default='📦', verbose_name='Ícone (emoji)')
    cor = models.CharField(max_length=7, default='#6B7280', verbose_name='Cor (hex)')
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def __str__(self):
        return self.nome


class Produto(models.Model):
    """
    Representa um produto no estoque.
    Cada produto tem código, nome, preço, quantidade e outras informações.
    """

    UNIDADE_CHOICES = [
        ('un', 'Unidade'),
        ('kg', 'Quilograma'),
        ('g', 'Grama'),
        ('l', 'Litro'),
        ('ml', 'Mililitro'),
        ('m', 'Metro'),
        ('cm', 'Centímetro'),
        ('cx', 'Caixa'),
        ('pc', 'Pacote'),
        ('pr', 'Par'),
        ('jg', 'Jogo'),
    ]

    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('descontinuado', 'Descontinuado'),
    ]

    # Código único do produto (como um código de barras interno)
    codigo = models.CharField(max_length=50, unique=True, verbose_name='Código')

    # Nome e descrição do produto
    nome = models.CharField(max_length=200, verbose_name='Nome')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descrição')

    # Categoria e fornecedor (relacionamentos com outros modelos)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,  # Se a categoria for excluída, o produto fica sem categoria
        null=True,
        blank=True,
        verbose_name='Categoria'
    )
    fornecedor = models.ForeignKey(
        Fornecedor,
        on_delete=models.SET_NULL,  # Se o fornecedor for excluído, o produto fica sem fornecedor
        null=True,
        blank=True,
        verbose_name='Fornecedor'
    )

    # Preços
    preco_custo = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name='Preço de Custo (R$)'
    )
    preco_venda = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name='Preço de Venda (R$)'
    )

    # Estoque
    quantidade = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name='Quantidade em Estoque'
    )
    estoque_minimo = models.DecimalField(
        max_digits=10, decimal_places=2, default=5,
        verbose_name='Estoque Mínimo (alerta)'
    )
    estoque_maximo = models.DecimalField(
        max_digits=10, decimal_places=2, default=100,
        verbose_name='Estoque Máximo'
    )

    # Unidade de medida (kg, litros, unidades, etc.)
    unidade = models.CharField(
        max_length=5, choices=UNIDADE_CHOICES, default='un',
        verbose_name='Unidade de Medida'
    )

    # Localização física no estoque
    localizacao = models.CharField(
        max_length=100, blank=True, null=True,
        verbose_name='Localização (ex: Prateleira A3)'
    )

    # Código de barras (opcional)
    codigo_barras = models.CharField(
        max_length=50, blank=True, null=True,
        verbose_name='Código de Barras'
    )

    # Imagem do produto
    imagem = models.ImageField(
        upload_to='produtos/', blank=True, null=True,
        verbose_name='Imagem'
    )

    # Status e controle
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default='ativo',
        verbose_name='Status'
    )
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['nome']

    def __str__(self):
        return f'{self.codigo} - {self.nome}'

    @property
    def esta_abaixo_minimo(self):
        """Verifica se o produto está com estoque abaixo do mínimo (alerta vermelho)"""
        return self.quantidade <= self.estoque_minimo

    @property
    def esta_zerado(self):
        """Verifica se o produto está sem estoque"""
        return self.quantidade <= 0

    @property
    def margem_lucro(self):
        """Calcula a margem de lucro em porcentagem"""
        if self.preco_custo > 0:
            return ((self.preco_venda - self.preco_custo) / self.preco_custo) * 100
        return 0

    @property
    def valor_estoque(self):
        """Calcula o valor total em estoque (quantidade × preço de custo)"""
        return self.quantidade * self.preco_custo

    @property
    def status_estoque(self):
        """Retorna o status do estoque para exibição colorida"""
        if self.esta_zerado:
            return 'zerado'
        elif self.esta_abaixo_minimo:
            return 'critico'
        elif self.quantidade <= self.estoque_minimo * 1.5:
            return 'alerta'
        else:
            return 'normal'
