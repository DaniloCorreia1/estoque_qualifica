"""
wsgi.py - Ponto de entrada para servidores web em produção (PythonAnywhere usa isso)
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'estoque_qualifica.settings')
application = get_wsgi_application()
