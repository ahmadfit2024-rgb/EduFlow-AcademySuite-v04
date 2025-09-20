import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')

# --- Core Settings ---
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key-for-development')
DEBUG = os.getenv('DEBUG', 'True') == 'True'
ALLOWED_HOSTS = []

# --- Application Definitions ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',

    # Local apps (Services)
    'apps.core',
    'apps.users',
    'apps.learning',
    'apps.enrollment',
    'apps.interactions',
    'apps.reports',
    'apps.contracts', # New app added here
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

ROOT_URLCONF = 'academy_suite.urls'

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
            'libraries':{
                'discussion_tags': 'apps.interactions.templatetags.discussion_tags',
            }
        },
    },
]

WSGI_APPLICATION = 'academy_suite.wsgi.application'

# --- Database (MongoDB with Djongo) ---
DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': os.getenv('DB_NAME', 'eduflow_db'),
        'ENFORCE_SCHEMA': False,
        'CLIENT': {
            'host': os.getenv('DB_HOST', 'mongodb://localhost:27017/'),
        }
    }
}

# --- Authentication ---
AUTH_USER_MODEL = 'users.CustomUser'

# --- Password validation ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internationalization (i18n) & Localization (l10n) ---
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Static files (CSS, JavaScript, Images) ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

# --- Media files (User Uploads) ---
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# --- Default primary key field type ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'