"""
fornecedores/models.py - Modelo de Fornecedor
Define a estrutura de dados dos fornecedores no banco de dados
"""
from django.db import models


class Fornecedor(models.Model):
    """
    Representa uma empresa ou pessoa que fornece produtos para o estoque.
    Pode ser um atacadista, fabricante, importador, etc.
    """

    # Tipo de pessoa jurídica ou física
    TIPO_CHOICES = [
        ('PJ', 'Pessoa Jurídica'),
        ('PF', 'Pessoa Física'),
    ]

    # Status do fornecedor
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('bloqueado', 'Bloqueado'),
    ]

    # Nome da empresa ou pessoa
    nome = models.CharField(max_length=200, verbose_name='Nome/Razão Social')

    # Nome fantasia (apelido da empresa)
    nome_fantasia = models.CharField(
        max_length=200, blank=True, null=True, verbose_name='Nome Fantasia'
    )

    # CPF ou CNPJ
    tipo = models.CharField(max_length=2, choices=TIPO_CHOICES, default='PJ', verbose_name='Tipo')
    documento = models.CharField(max_length=20, blank=True, null=True, verbose_name='CPF/CNPJ')

    # Informações de contato
    email = models.EmailField(blank=True, null=True, verbose_name='E-mail')
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone')
    celular = models.CharField(max_length=20, blank=True, null=True, verbose_name='Celular')

    # Endereço completo
    cep = models.CharField(max_length=10, blank=True, null=True, verbose_name='CEP')
    endereco = models.CharField(max_length=300, blank=True, null=True, verbose_name='Endereço')
    numero = models.CharField(max_length=20, blank=True, null=True, verbose_name='Número')
    complemento = models.CharField(max_length=100, blank=True, null=True, verbose_name='Complemento')
    bairro = models.CharField(max_length=100, blank=True, null=True, verbose_name='Bairro')
    cidade = models.CharField(max_length=100, blank=True, null=True, verbose_name='Cidade')
    estado = models.CharField(max_length=2, blank=True, null=True, verbose_name='Estado')

    # Informações comerciais
    prazo_entrega = models.IntegerField(
        default=0, verbose_name='Prazo de Entrega (dias)'
    )
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')

    # Status e controle
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ativo', verbose_name='Status')
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Fornecedor'
        verbose_name_plural = 'Fornecedores'
        ordering = ['nome']

    def __str__(self):
        """Retorna o nome do fornecedor para exibição"""
        return self.nome_fantasia or self.nome

    @property
    def total_produtos(self):
        """Conta quantos produtos esse fornecedor tem no sistema"""
        return self.produto_set.count()
