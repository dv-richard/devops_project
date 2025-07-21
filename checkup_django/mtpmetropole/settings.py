import os
from pathlib import Path
from dotenv import load_dotenv

# ──────────────────────────────────────────────────────────────────────────────
# Chargement des variables d’environnement depuis .env
# ──────────────────────────────────────────────────────────────────────────────

load_dotenv()

# Vos identifiants et URLs OIDC
OIDC_RP_CLIENT_ID               = os.getenv('OIDC_CLIENT_ID')
OIDC_RP_CLIENT_SECRET           = os.getenv('OIDC_CLIENT_SECRET')
OIDC_RP_CALLBACK_URI            = os.getenv('OIDC_RP_CALLBACK_URI')

OIDC_OP_AUTHORIZATION_ENDPOINT  = os.getenv('OIDC_OP_AUTHORIZATION_ENDPOINT')
OIDC_OP_TOKEN_ENDPOINT          = os.getenv('OIDC_TOKEN_ENDPOINT')
OIDC_OP_USERINFO_ENDPOINT       = os.getenv('OIDC_USER_ENDPOINT')

# Forcer la vérification SSL sur les échanges token (à False en local si besoin)
OIDC_OP_SSL                     = os.getenv('OIDC_OP_SSL', 'False') == 'True'


# ──────────────────────────────────────────────────────────────────────────────
# BASE SETTINGS
# ──────────────────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = int(os.environ.get("DEBUG", default=0))

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '').split(',')

CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', '').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'simple_history',
    'checklist',
    'djangosaml2',
    'rest_framework',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'djangosaml2.middleware.SamlSessionMiddleware',
    'simple_history.middleware.HistoryRequestMiddleware',
]

ROOT_URLCONF = 'mtpmetropole.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'checklist' / 'templates' / 'checklist' ],
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

WSGI_APPLICATION = 'mtpmetropole.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db', 'database.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'fr'
TIME_ZONE     = 'Europe/Paris'
USE_I18N      = True
USE_TZ        = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / 'checklist' / 'static']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ──────────────────────────────────────────────────────────────────────────────
# Django REST Framework
# ──────────────────────────────────────────────────────────────────────────────

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}


# ──────────────────────────────────────────────────────────────────────────────
# Authentification & SSO
# ──────────────────────────────────────────────────────────────────────────────

# Redirection en cas de @login_required
LOGIN_URL = '/oidc/login/'

# Ré-exposer clairement pour vos vues
OIDC_AUTH_ENDPOINT         = OIDC_OP_AUTHORIZATION_ENDPOINT
OIDC_TOKEN_ENDPOINT        = OIDC_OP_TOKEN_ENDPOINT
OIDC_USERINFO_ENDPOINT     = OIDC_OP_USERINFO_ENDPOINT
OIDC_REDIRECT_URI          = OIDC_RP_CALLBACK_URI

CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')
CORS_ALLOW_CREDENTIALS = True 