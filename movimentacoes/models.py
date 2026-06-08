"""
movimentacoes/models.py - Modelo de Movimentação de Estoque
Registra toda entrada e saída de produtos
"""
from django.db import models
from django.conf import settings
from produtos.models import Produto


class Movimentacao(models.Model):
    """
    Registra cada movimentação de estoque.
    Toda vez que um produto entra ou sai do estoque, cria-se um registro aqui.
    """

    TIPO_CHOICES = [
        ('entrada', 'Entrada'),
        ('saida', 'Saída'),
        ('ajuste', 'Ajuste de Inventário'),
        ('devolucao', 'Devolução'),
        ('perda', 'Perda/Avaria'),
        ('transferencia', 'Transferência'),
    ]

    MOTIVO_ENTRADA = [
        ('compra', 'Compra'),
        ('devolucao_cliente', 'Devolução de Cliente'),
        ('ajuste_positivo', 'Ajuste Positivo'),
        ('transferencia_entrada', 'Transferência Recebida'),
        ('outros', 'Outros'),
    ]

    MOTIVO_SAIDA = [
        ('venda', 'Venda'),
        ('consumo_interno', 'Consumo Interno'),
        ('devolucao_fornecedor', 'Devolução ao Fornecedor'),
        ('perda', 'Perda/Avaria'),
        ('ajuste_negativo', 'Ajuste Negativo'),
        ('transferencia_saida', 'Transferência Enviada'),
        ('outros', 'Outros'),
    ]

    # Qual produto foi movimentado
    produto = models.ForeignKey(
        Produto,
        on_delete=models.PROTECT,  # Não deixa excluir produto que tem movimentação
        verbose_name='Produto'
    )

    # Tipo de movimentação (entrada ou saída)
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, verbose_name='Tipo')

    # Motivo da movimentação
    motivo = models.CharField(max_length=30, verbose_name='Motivo')

    # Quantidade movimentada
    quantidade = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name='Quantidade'
    )

    # Preço unitário no momento da movimentação
    preco_unitario = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name='Preço Unitário (R$)'
    )

    # Estoque antes e depois (para histórico)
    estoque_anterior = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name='Estoque Anterior'
    )
    estoque_posterior = models.DecimalField(
        max_digits=10, decimal_places=2, default=0,
        verbose_name='Estoque Posterior'
    )

    # Número de documento (nota fiscal, pedido, etc.)
    numero_documento = models.CharField(
        max_length=100, blank=True, null=True,
        verbose_name='Nº Documento (NF, Pedido...)'
    )

    # Observações
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações')

    # Quem fez a movimentação
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Usuário'
    )

    # Data e hora da movimentação
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Data/Hora')

    class Meta:
        verbose_name = 'Movimentação'
        verbose_name_plural = 'Movimentações'
        ordering = ['-criado_em']  # Mais recentes primeiro

    def __str__(self):
        return f'{self.get_tipo_display()} - {self.produto.nome} ({self.quantidade} {self.produto.unidade})'

    @property
    def valor_total(self):
        """Calcula o valor total da movimentação"""
        return self.quantidade * self.preco_unitario

    def save(self, *args, **kwargs):
        """
        Sobrescreve o save para atualizar o estoque do produto automaticamente.
        Isso é chamado automaticamente quando a movimentação é salva.
        """
        produto = self.produto

        # Guarda o estoque antes de alterar
        self.estoque_anterior = produto.quantidade

        # Se é uma movimentação nova (não é edição)
        if not self.pk:
            if self.tipo == 'entrada' or self.tipo == 'devolucao':
                # Entrada: soma ao estoque
                produto.quantidade += self.quantidade
            elif self.tipo in ['saida', 'perda', 'transferencia']:
                # Saída: subtrai do estoque
                produto.quantidade -= self.quantidade
            elif self.tipo == 'ajuste':
                # Ajuste: define o valor exato
                produto.quantidade = self.quantidade

            # Guarda o estoque depois de alterar
            self.estoque_posterior = produto.quantidade
            # Salva o produto com o novo estoque
            produto.save()

        super().save(*args, **kwargs)
