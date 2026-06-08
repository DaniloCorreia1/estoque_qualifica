"""
settings.py - Configurações principais do projeto Django
Aqui ficam todas as configurações do sistema: banco de dados, apps, segurança, etc.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env (onde ficam senhas e chaves de API)
load_dotenv()

# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Chave secreta do Django - NUNCA coloque isso em produção no código diretamente
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-estoque-qualifica-chave-padrao-trocar-em-producao')

# DEBUG = True durante desenvolvimento, False em produção
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Hosts permitidos para acessar o sistema
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.pythonanywhere.com', '*']

# ============================================================
# APPS INSTALADOS - Todos os módulos do sistema
# ============================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Apps do nosso sistema
    'core',           # App principal: dashboard, home
    'accounts',       # App de usuários e autenticação
    'fornecedores',   # App de fornecedores
    'produtos',       # App de produtos
    'movimentacoes',  # App de movimentações (entrada/saída)
    'relatorios',     # App de relatórios
]

# ============================================================
# MIDDLEWARES - Camadas de processamento de requisições
# ============================================================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Para servir arquivos estáticos
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'estoque_qualifica.urls'

# ============================================================
# TEMPLATES - Configuração dos arquivos HTML
# ============================================================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Pasta onde ficam os HTMLs
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'estoque_qualifica.wsgi.application'

# ============================================================
# BANCO DE DADOS - Usando SQLite (arquivo local, perfeito para começar)
# ============================================================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Arquivo do banco na raiz do projeto
    }
}

# ============================================================
# VALIDAÇÃO DE SENHA
# ============================================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Modelo de usuário personalizado
AUTH_USER_MODEL = 'accounts.Usuario'

# Idioma e fuso horário
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ============================================================
# ARQUIVOS ESTÁTICOS (CSS, JS, imagens)
# ============================================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Onde ficam após o collectstatic

# WhiteNoise para servir estáticos em produção
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ============================================================
# ARQUIVOS DE MÍDIA (uploads de imagens)
# ============================================================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Chave da API OpenAI - pegue em https://platform.openai.com
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

# Páginas de login/logout
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/accounts/login/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuração de mensagens do Django
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}
