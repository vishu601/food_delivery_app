from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-jw91(7kfhg=do_zekj0*8%x=e*wzej0emhj*0od351h8!cr1^1'

# 1. DEBUG MODE ON (Ab har error khul kar dikhega)
DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',      # Sahi order mein configuration
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'foodapp',
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

ROOT_URLCONF = 'food_project.urls'

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

WSGI_APPLICATION = 'food_project.wsgi.application'

# 2. DOCKER POSTGRESQL DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'food_delivery_db',      # docker-compose mein POSTGRES_DB hai
        'USER': 'admin',                 # docker-compose mein POSTGRES_USER hai
        'PASSWORD': 'Admin@123',         # docker-compose mein POSTGRES_PASSWORD hai
        'HOST': 'db',                    # Docker service name
        'PORT': '5432',                  # PostgreSQL ka default internal port
    }
}

# Baki ka password validators aur localizations bilkul purane code ki tarah rehne dena niche...





STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'