import os
from pathlib import Path
from dotenv import load_dotenv

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Tenta carregar o arquivo .env
dotenv_path = os.path.join(BASE_DIR, '.env')
load_dotenv(dotenv_path)

# --- SEGURANÇA ---
# Em produção, usamos a chave do .env. Se não achar, usa a padrão (evita erro)
SECRET_KEY = os.getenv(
    'SECRET_KEY', 'django-insecure-24zdo%4hu76s97ad4n#f^p!!a^ku3^@_!y#(rlk3e4yb!dizn4')

# MUDANÇA PARA DEPLOY: DEBUG deve ser False em produção
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Liberar o domínio do Railway e o acesso local
# Depois de subir, você pode colocar ['seu-projeto.up.railway.app', 'localhost']
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'whitenoise.runserver_nostatic',  # Adicionado para arquivos estáticos
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # Adicionado para servir CSS/JS no deploy
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
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'setup.wsgi.application'

# Database - Railway (Puxando via ENV para segurança)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'railway'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'akIJnidbwTSajgkJOyjiuCdLaCXzCCAF'),
        'HOST': os.getenv('DB_HOST', 'ballast.proxy.rlwy.net'),
        'PORT': os.getenv('DB_PORT', '12135'),
    }
}

# Configurações Jazzmin (Mantidas como você pediu)
JAZZMIN_SETTINGS = {
    "site_title": "Admin Portfólio",
    "site_header": "Washington",
    "site_brand": "Dashboard Tom",
    "site_logo": None,
    "login_logo": None,
    "site_logo_login": None,
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

# --- ARQUIVOS ESTÁTICOS EM PRODUÇÃO ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
# Pasta onde o Django vai reunir o CSS para o deploy
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
