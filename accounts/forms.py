"""
accounts/forms.py - Formulários de usuário
Os formulários validam os dados antes de salvar no banco de dados
"""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import Usuario


class LoginForm(AuthenticationForm):
    """
    Formulário de login.
    Herda do formulário padrão do Django e personaliza o visual.
    """
    username = forms.CharField(
        label='Usuário',
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-green-400',
            'placeholder': 'Digite seu usuário',
            'autofocus': True
        })
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 bg-gray-800 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-green-400',
            'placeholder': 'Digite sua senha'
        })
    )


class CadastroUsuarioForm(UserCreationForm):
    """
    Formulário para cadastrar novos usuários.
    Herda do formulário de criação de usuário do Django.
    """
    first_name = forms.CharField(
        label='Nome',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Primeiro nome'
        })
    )
    last_name = forms.CharField(
        label='Sobrenome',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Sobrenome'
        })
    )
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'email@exemplo.com'
        })
    )
    telefone = forms.CharField(
        label='Telefone',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '(61) 99999-9999'
        })
    )
    departamento = forms.CharField(
        label='Departamento',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Ex: Almoxarifado'
        })
    )
    perfil = forms.ChoiceField(
        label='Perfil',
        choices=Usuario.PERFIL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-input'})
    )
    foto = forms.ImageField(
        label='Foto de Perfil',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-input'})
    )

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'telefone',
                  'departamento', 'perfil', 'foto', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personaliza os campos de senha
        self.fields['username'].widget.attrs['class'] = 'form-input'
        self.fields['username'].label = 'Nome de usuário'
        self.fields['password1'].widget.attrs['class'] = 'form-input'
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].widget.attrs['class'] = 'form-input'
        self.fields['password2'].label = 'Confirmar senha'


class EdicaoUsuarioForm(forms.ModelForm):
    """Formulário para editar dados de um usuário existente"""

    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'telefone', 'departamento', 'perfil', 'foto']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'telefone': 'Telefone',
            'departamento': 'Departamento',
            'perfil': 'Perfil',
            'foto': 'Foto de Perfil',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'telefone': forms.TextInput(attrs={'class': 'form-input'}),
            'departamento': forms.TextInput(attrs={'class': 'form-input'}),
            'perfil': forms.Select(attrs={'class': 'form-input'}),
            'foto': forms.FileInput(attrs={'class': 'form-input'}),
        }
