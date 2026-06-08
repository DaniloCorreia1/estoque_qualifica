"""
fornecedores/forms.py - Formulário de fornecedor
"""
from django import forms
from .models import Fornecedor


class FornecedorForm(forms.ModelForm):
    """Formulário para criar e editar fornecedores"""

    class Meta:
        model = Fornecedor
        fields = [
            'nome', 'nome_fantasia', 'tipo', 'documento',
            'email', 'telefone', 'celular',
            'cep', 'endereco', 'numero', 'complemento', 'bairro', 'cidade', 'estado',
            'prazo_entrega', 'status', 'observacoes'
        ]
        labels = {
            'nome': 'Nome/Razão Social',
            'nome_fantasia': 'Nome Fantasia',
            'tipo': 'Tipo',
            'documento': 'CPF/CNPJ',
            'prazo_entrega': 'Prazo de Entrega (dias)',
        }
        widgets = {
            # Todos os campos recebem a classe CSS 'form-input' para estilização uniforme
            'nome': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Razão social ou nome completo'}),
            'nome_fantasia': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Nome fantasia (opcional)'}),
            'tipo': forms.Select(attrs={'class': 'form-input'}),
            'documento': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '00.000.000/0001-00'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'email@empresa.com'}),
            'telefone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '(61) 3000-0000'}),
            'celular': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '(61) 99999-9999'}),
            'cep': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '70000-000', 'id': 'id_cep'}),
            'endereco': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Rua, Avenida...', 'id': 'id_endereco'}),
            'numero': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '123'}),
            'complemento': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Sala, Andar...'}),
            'bairro': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Bairro', 'id': 'id_bairro'}),
            'cidade': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Cidade', 'id': 'id_cidade'}),
            'estado': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'DF', 'maxlength': '2', 'id': 'id_estado'}),
            'prazo_entrega': forms.NumberInput(attrs={'class': 'form-input', 'min': '0'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Informações adicionais...'}),
        }
