import os
from pathlib import Path
from django.contrib.messages import constants as messages
from dotenv import load_dotenv

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# --- CARREGAR VARIÁVEIS DO .ENV ---
load_dotenv(os.path.join(BASE_DIR, '.env'))

# --- FUNÇÃO PARA LIMPAR ASPAS DO RAILWAY ---


def clean_env(name, default=None):
    value = os.getenv(name, default)
    if value and isinstance(value, str):
        return value.strip('"').strip("'")
    return value


# --- SEGURANÇA ---
SECRET_KEY = clean_env('SECRET_KEY', 'django-insecure-24zdo%4hu76s97ad4n')
DEBUG = clean_env('DEBUG', 'False').upper() == 'TRUE'

ALLOWED_HOSTS = ['*', '.up.railway.app']

# Essencial para CSRF no Railway
CSRF_TRUSTED_ORIGINS = [
    'https://portfolio-profissional-production.up.railway.app',
    'https://*.up.railway.app'
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

# Database - Configuração para Railway (MySQL) com Limpeza de Aspas
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': clean_env('DB_NAME', 'railway'),
        'USER': clean_env('DB_USER', 'root'),
        'PASSWORD': clean_env('DB_PASSWORD'),
        'HOST': clean_env('DB_HOST'),
        'PORT': clean_env('DB_PORT', '12135'),  # Porta do seu .env
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

# --- CONFIGURAÇÕES DE E-MAIL (GMAIL) ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = clean_env('EMAIL_USER')
EMAIL_HOST_PASSWORD = clean_env('EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

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
    "copyright": "Washington 2025",
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
