#!/usr/bin/env python
"""
manage.py - Ferramenta de linha de comando do Django
Usada para: rodar o servidor, criar migrações, criar superusuário, etc.
Exemplos:
    python manage.py runserver      -> inicia o servidor local
    python manage.py makemigrations -> cria arquivos de migração do banco
    python manage.py migrate        -> aplica as migrações no banco
    python manage.py createsuperuser -> cria um usuário administrador
"""
import os
import sys


def main():
    """Função principal que executa os comandos do Django."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estoque_qualifica.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Não foi possível importar o Django. Verifique se ele está instalado "
            "e se o ambiente virtual está ativado."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
