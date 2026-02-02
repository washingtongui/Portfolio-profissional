import os
from pathlib import Path
from django.contrib.messages import constants as messages
from dotenv import load_dotenv
import pymysql
import dj_database_url

# --- HACK PARA DJANGO 6.0+ E PYMySQL ---
# Engana o Django para aceitar o PyMySQL como se fosse o mysqlclient moderno
pymysql.version_info = (2, 2, 1, "final", 0)
pymysql.install_as_MySQLdb()

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# --- CARREGAR VARIÁVEIS DO .ENV ---
load_dotenv(BASE_DIR / '.env')

# --- FUNÇÃO PARA LIMPAR ASPAS E ESPAÇOS ---


def clean_env(name, default=None):
    value = os.getenv(name, default)
    if value:
        return str(value).strip('"').strip("'").strip()
    return value


# --- SEGURANÇA ---
SECRET_KEY = clean_env('SECRET_KEY', 'django-insecure-24zdo%4hu76s97ad4n')
DEBUG = clean_env('DEBUG', 'True').upper() == 'TRUE'

ALLOWED_HOSTS = ['*', '.up.railway.app']

# Essencial para CSRF no Railway
CSRF_TRUSTED_ORIGINS = [
    'https://portfolio-profissional-production.up.railway.app',
    'https://*.up.railway.app',
    'http://localhost',
    'http://127.0.0.1'
]

# Application definition
INSTALLED_APPS = [
    'whitenoise.runserver_nostatic',
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'setup.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'setup.wsgi.application'

# --- BANCO DE DADOS (PROTEÇÃO CONTRA CACHE DE IP INTERNO) ---
# Se estiver no Railway (Produção), ele usa a URL completa.
# Se estiver no seu PC, ele ignora o cache do Windows e usa o host do .env.
if os.getenv('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(conn_max_age=600)
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': clean_env('DB_NAME', 'railway'),
            'USER': clean_env('DB_USER', 'root'),
            'PASSWORD': clean_env('DB_PASSWORD'),
            'HOST': clean_env('DB_HOST', 'tramway.proxy.rlwy.net'),
            'PORT': clean_env('DB_PORT', '31483'),
            'OPTIONS': {
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
                'charset': 'utf8mb4',
            },
        }
    }

# --- ARQUIVOS ESTÁTICOS ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# --- CONFIGURAÇÃO DE E-MAIL (RESEND API) ---
RESEND_API_KEY = clean_env('RESEND_API_KEY')
DEFAULT_FROM_EMAIL = "onboarding@resend.dev"

# Localização
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
    messages.SUCCESS: 'success',
}

# JAZZMIN SETTINGS
JAZZMIN_SETTINGS = {
    "site_title": "Admin Portfólio",
    "site_header": "Washington",
    "site_brand": "Dashboard Tom",
    "welcome_sign": "Bem-vindo ao Gerenciamento do seu Portfólio",
    "copyright": "Washington 2026",
    "show_sidebar": True,
    "navigation_expanded": True,
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "core.Contato": "fas fa-envelope",
    },
    "topmenu_links": [
        {"name": "Ver Site", "url": "/", "new_window": True},
    ],
}
