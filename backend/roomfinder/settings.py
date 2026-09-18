"""
Django settings for roomfinder project.
"""

from pathlib import Path

# backend/roomfinder/settings.py -> BASE_DIR = backend/
BASE_DIR = Path(__file__).resolve().parent.parent

# Room Finder/ (one level above backend/) - where frontend/ and media/ live
PROJECT_ROOT = BASE_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / 'frontend'

# SECURITY WARNING: keep this secret in real deployment (fine for local dev/college project)
SECRET_KEY = 'django-insecure-change-this-key-for-production-use-only'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps
    'properties',
    # 'accounts',      # add once teammate's accounts app is ready
    # 'dashboard',     # add once teammate's dashboard app is ready
    # 'chat',          # add once teammate's chat app is ready
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'roomfinder.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [FRONTEND_DIR / 'templates'],
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

WSGI_APPLICATION = 'roomfinder.wsgi.application'

# Database - SQLite (default, file created automatically on first migrate)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kathmandu'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript)
STATIC_URL = 'static/'
STATICFILES_DIRS = [FRONTEND_DIR / 'static']

# Media files (user-uploaded property images)
MEDIA_URL = '/media/'
MEDIA_ROOT = PROJECT_ROOT / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# NOTE for accounts-app teammate:
# If/when a custom User model is created, set AUTH_USER_MODEL = 'accounts.User' here
# BEFORE running your first migration on a fresh database (switching later requires
# resetting migrations + deleting db.sqlite3).
