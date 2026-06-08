"""
movimentacoes/forms.py - Formulários de movimentação
"""
from django import forms
from .models import Movimentacao


class EntradaForm(forms.ModelForm):
    """Formulário para registrar entrada de produtos"""
    class Meta:
        model = Movimentacao
        fields = ['produto', 'quantidade', 'motivo', 'preco_unitario', 'numero_documento', 'observacoes']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-input'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0.01'}),
            'motivo': forms.Select(
                choices=Movimentacao.MOTIVO_ENTRADA,
                attrs={'class': 'form-input'}
            ),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'NF, Pedido...'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }
        labels = {
            'preco_unitario': 'Preço Unitário (R$)',
            'numero_documento': 'Nº Documento',
        }


class SaidaForm(forms.ModelForm):
    """Formulário para registrar saída de produtos"""
    class Meta:
        model = Movimentacao
        fields = ['produto', 'quantidade', 'motivo', 'preco_unitario', 'numero_documento', 'observacoes']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-input'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0.01'}),
            'motivo': forms.Select(
                choices=Movimentacao.MOTIVO_SAIDA,
                attrs={'class': 'form-input'}
            ),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'numero_documento': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'NF, Pedido...'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
        }
        labels = {
            'preco_unitario': 'Preço Unitário (R$)',
            'numero_documento': 'Nº Documento',
        }


class AjusteForm(forms.ModelForm):
    """Formulário para ajuste de inventário"""
    class Meta:
        model = Movimentacao
        fields = ['produto', 'quantidade', 'observacoes']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-input'}),
            'quantidade': forms.NumberInput(attrs={
                'class': 'form-input', 'step': '0.01', 'min': '0',
                'placeholder': 'Nova quantidade real do estoque'
            }),
            'observacoes': forms.Textarea(attrs={
                'class': 'form-input', 'rows': 3,
                'placeholder': 'Motivo do ajuste (ex: contagem física revelou diferença)'
            }),
        }
        labels = {
            'quantidade': 'Nova Quantidade (valor real contado)',
        }
