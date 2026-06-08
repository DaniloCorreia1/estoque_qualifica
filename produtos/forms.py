"""
produtos/forms.py - Formulários de produto e categoria
"""
from django import forms
from .models import Produto, Categoria


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = [
            'codigo', 'nome', 'descricao', 'categoria', 'fornecedor',
            'preco_custo', 'preco_venda', 'quantidade', 'estoque_minimo',
            'estoque_maximo', 'unidade', 'localizacao', 'codigo_barras',
            'imagem', 'status'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: PROD-001'}),
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome do produto'}),
            'descricao': forms.Textarea(attrs={'class': 'form-input', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-input'}),
            'fornecedor': forms.Select(attrs={'class': 'form-input'}),
            'preco_custo': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'preco_venda': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'estoque_minimo': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'estoque_maximo': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'min': '0'}),
            'unidade': forms.Select(attrs={'class': 'form-input'}),
            'localizacao': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Ex: Prateleira A3'}),
            'codigo_barras': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Código de barras'}),
            'imagem': forms.FileInput(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
        }


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao', 'icone', 'cor']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome da categoria'}),
            'descricao': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
            'icone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '📦'}),
            'cor': forms.TextInput(attrs={'class': 'form-input', 'type': 'color'}),
        }
