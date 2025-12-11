from pathlib import Path
import os
BASE_DIR = Path(__file__).resolve().parent.parent


print("DEBUG STATIC ROOT")
print("BASE_DIR:", BASE_DIR)
print("STATIC_ROOT:", STATIC_ROOT)

SECRET_KEY = 'django-insecure-l@sm*gmiymv_dj!a8+p&a$ai#59ymxb6+pi)^r5z+5fq$g)d(4'
DEBUG = True

ALLOWED_HOSTS = [
    'kristynaglacova.pythonanywhere.com',
    '127.0.0.1',
    'localhost'
]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
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

ROOT_URLCONF = 'projectdjango.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'projectdjango.wsgi.application'


# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# LOGIN
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = 'login'


# STATIC FILES

STATIC_URL = '/static/'

# Cesty k statickým souborům uvnitř aplikace
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'store', 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Kam Django zkopíruje všechny statické soubory při collectstatic

# MEDIA
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR / "static",  
]

BASE_DIR = Path(__file__).resolve().parent.parent
