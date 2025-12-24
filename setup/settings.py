import os
from pathlib import Path
from dotenv import load_dotenv
from django.contrib.messages import constants as messages

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Tenta carregar o arquivo .env (Apenas para local)
dotenv_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# --- SEGURANÇA ---
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-24zdo%4hu76s97ad4n')

# No Railway, forçamos True agora para ver o erro real se ele persistir
DEBUG = os.getenv('DEBUG', 'True').upper() == 'TRUE'

# Domínios permitidos
ALLOWED_HOSTS = [
    '*', 'portfolio-profissional-production.up.railway.app', '.up.railway.app']

# Essencial para HTTPS e formulários no Railway
CSRF_TRUSTED_ORIGINS = [
    'https://portfolio-profissional-production.up.railway.app', 'https://*.up.railway.app']

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

# Database - Configuração Robusta para Railway
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'railway'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

# --- CONFIGURAÇÕES DO JAZZMIN ---
JAZZMIN_SETTINGS = {
    "site_title": "Admin Portfólio",
    "site_header": "Washington",
    "site_brand": "Dashboard Tom",
    "welcome_sign": "Bem-vindo ao Gerenciamento do seu Portfólio",
    "copyright": "Washington 2025",
    "search_model": ["core.Contato"],
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

JAZZMIN_UI_CONFIG = {
    "theme": "flatly",
    "dark_mode_theme": "darkly",
}

# --- ARQUIVOS ESTÁTICOS ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Armazenamento otimizado para produção
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# --- CONFIGURAÇÕES DE E-MAIL ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')

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
