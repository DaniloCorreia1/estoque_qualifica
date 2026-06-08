"""
accounts/models.py - Modelos de usuário do sistema
Define como os usuários são armazenados no banco de dados
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    """
    Modelo de usuário personalizado.
    Herda tudo do usuário padrão do Django e adiciona campos extras.
    AbstractUser já tem: username, email, password, first_name, last_name, is_active, is_staff
    """

    # Tipos de perfil de usuário
    PERFIL_CHOICES = [
        ('admin', 'Administrador'),
        ('funcionario', 'Funcionário'),
    ]

    # Campo de perfil - define o nível de acesso
    perfil = models.CharField(
        max_length=20,
        choices=PERFIL_CHOICES,
        default='funcionario',
        verbose_name='Perfil'
    )

    # Telefone do usuário
    telefone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Telefone'
    )

    # Departamento onde trabalha
    departamento = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name='Departamento'
    )

    # Foto de perfil
    foto = models.ImageField(
        upload_to='fotos_usuarios/',
        blank=True,
        null=True,
        verbose_name='Foto de Perfil'
    )

    # Data de quando foi cadastrado no sistema
    criado_em = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')

    # Data da última atualização
    atualizado_em = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        ordering = ['first_name']

    def __str__(self):
        """Retorna o nome completo ou username para identificar o usuário"""
        return self.get_full_name() or self.username

    @property
    def is_admin(self):
        """Verifica se o usuário é administrador"""
        return self.perfil == 'admin' or self.is_superuser

    @property
    def nome_exibicao(self):
        """Nome para exibir na tela"""
        return self.get_full_name() or self.username
