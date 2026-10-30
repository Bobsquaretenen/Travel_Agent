"""
Django settings for travel_project project.
"""

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-n4mtbz!t+7ltk4d(p8#e3ls6rgtmd14@k^rgdgvp7oe4ej5wk9')

DEBUG = False

ALLOWED_HOSTS = ['.netrun.io', '127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'travel_agent',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # ВАЖНО: WhiteNoise должен идти сразу после SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'travel_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'travel' / 'templates'],
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

WSGI_APPLICATION = 'travel_project.wsgi.application'

# База данных (для Netrun)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/data/db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTH_USER_MODEL = 'travel_agent.User'

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# ============================================
# НАСТРОЙКИ СТАТИКИ (ИСПРАВЛЕНО)
# ============================================
STATIC_URL = '/static/'

# Папка, где лежат ваши исходные CSS/JS (для локальной разработки)
STATICFILES_DIRS = [BASE_DIR / 'static']

# Папка, куда collectstatic будет собирать все файлы для продакшена
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Включаем сжатие и кэширование статики через WhiteNoise
# (Используем CompressedStaticFilesStorage, чтобы избежать ошибок с путями)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

# Медиафайлы (загруженные пользователями картинки)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTHENTICATION_BACKENDS = [
    'travel_agent.backends.EmailOrUsernameBackend',
    'django.contrib.auth.backends.ModelBackend',
]

CSRF_FAILURE_VIEW = 'travel_agent.views.csrf_failure'