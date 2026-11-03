"""
Django settings for travel_project project.
"""
from pathlib import Path
import os
import dj_database_url # <-- ДОБАВЛЕНО ДЛЯ RENDER

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ (берется из переменных окружения на сервере)
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-n4mtbz!t+7ltk4d(p8#e3ls6rgtmd14@k^rgdgvp7oe4ej5wk9')

# ВАЖНО: Для продакшена всегда False
DEBUG = False

# Разрешаем запросы с Render и локально
ALLOWED_HOSTS = ['.onrender.com', '.netrun.io', '127.0.0.1', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'csp',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'travel_agent',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # ВАЖНО: WhiteNoise должен идти сразу после SecurityMiddleware
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'csp.middleware.CSPMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'travel_agent.middleware.SecurityHeadersMiddleware',
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

# База данных: Render автоматически передает DATABASE_URL для PostgreSQL
DATABASES = {
    'default': dj_database_url.config(
        # Если DATABASE_URL нет (локальная разработка), используем SQLite
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600
    )
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

# Настройки статики (CSS, JS, Картинки)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles' # Сюда collectstatic соберет файлы
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Медиа (загруженные картинки туров)
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

# Перенаправлять весь HTTP-трафик на HTTPS
SECURE_SSL_REDIRECT = True

# HSTS (Strict-Transport-Security): заставляем браузер использовать только HTTPS
SECURE_HSTS_SECONDS = 31536000  # 1 год (рекомендуемое значение)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Защита от MIME-sniffing (уже включена по умолчанию, но фиксируем явно)
SECURE_CONTENT_TYPE_NOSNIFF = True

# Безопасные Cookies (работают только по HTTPS)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ["'self'"],
        "script-src": ["'self'"],
        "style-src": [
            "'self'",
            "'unsafe-inline'",  # Нужно для встроенных стилей (если есть)
            "https://fonts.googleapis.com",
        ],
        "font-src": [
            "'self'",
            "https://fonts.gstatic.com",
        ],
        "img-src": [
            "'self'",
            "data:",
            "https://images.unsplash.com",  # Картинки с Unsplash
        ],
        "frame-src": [
            "'self'",
            "https://yandex.ru",  # Карта
        ],
        "connect-src": ["'self'"],
    }
}