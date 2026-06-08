# pythonanywhere_wsgi.py
# Cole o conteúdo deste arquivo no arquivo WSGI do PythonAnywhere
# Caminho: /var/www/SEU_USUARIO_pythonanywhere_com_wsgi.py

import sys
import os

# Caminho onde o projeto foi clonado no PythonAnywhere
# Substitua SEU_USUARIO pelo seu username do PythonAnywhere
PASTA_PROJETO = '/home/SEU_USUARIO/estoque_qualifica'

# Adiciona o projeto ao path do Python
if PASTA_PROJETO not in sys.path:
    sys.path.insert(0, PASTA_PROJETO)

# Ativa o ambiente virtual
VIRTUALENV = '/home/SEU_USUARIO/.virtualenvs/estoque_qualifica/lib/python3.10/site-packages'
if VIRTUALENV not in sys.path:
    sys.path.insert(0, VIRTUALENV)

# Define as variáveis de ambiente
os.environ['DJANGO_SETTINGS_MODULE'] = 'estoque_qualifica.settings'
os.environ['SECRET_KEY'] = 'sua-chave-secreta-aqui'
os.environ['DEBUG'] = 'False'
os.environ['OPENAI_API_KEY'] = 'sk-sua-chave-openai-aqui'

# Importa a aplicação WSGI do Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
