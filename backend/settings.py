from pathlib import Path
import os
from decouple import config
from datetime import timedelta
import dj_database_url
import cloudinary.api
import cloudinary.uploader
from cloudinary.models import CloudinaryField


# -------------------------------
# Paths
# -------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# -------------------------------
# Security
# -------------------------------
SECRET_KEY = config('SECRET_KEY', default='django-insecure-local-key')
DEBUG = config('DEBUG', default=True, cast=bool)
# Use your specific Render domain when DEBUG is False for security
ALLOWED_HOSTS = ['*'] 

# -------------------------------
# Applications
# -------------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'products',

    # 3rd party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'drf_spectacular',
    
    # Cloudinary for file storage (FREE, NO CREDIT CARD)
    'cloudinary_storage', 
    'cloudinary',
    
    # Optional: profiling
    'silk',
]

# -------------------------------
# Middleware
# -------------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # MUST come before other middleware that might consume the request body
    'corsheaders.middleware.CorsMiddleware',       
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'silk.middleware.SilkyMiddleware', 
]


# -------------------------------
# URLs & Templates
# -------------------------------
ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'

# -------------------------------
# Database (PostgreSQL)
# -------------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True  # Render PostgreSQL requires SSL
    )
}


# -------------------------------
# Password Validators
# -------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# -------------------------------
# Internationalization
# -------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# -------------------------------
# Static Files (Handled by Whitenoise)
# -------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# -------------------------------
# Media Files (Local vs. Cloudinary)
# -------------------------------

if DEBUG:
    # Local Development Settings (Uses local disk)
    MEDIA_URL = '/media/'
    MEDIA_ROOT = BASE_DIR / 'media'
else:
    # Production Settings (Uses Cloudinary for persistent storage)
    
    # 1. Cloudinary Credentials (Must be set as ENV vars on Render)
    CLOUDINARY_CLOUD_NAME = config('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = config('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = config('CLOUDINARY_API_SECRET')

    # 2. Configure Django to use Cloudinary for all media files
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    
    # 3. Set the base URL for media
    MEDIA_URL = '/media/'
    
    # Optional: Configure the folder inside Cloudinary (good practice)
    CLOUDINARY_STORAGE = {
        'MEDIA_FOLDER': 'e_commerce_media',
        'STATIC_FOLDER': 'e_commerce_static',
        # You can add other options here if needed, like transformations
    }
    
    # Initialize the cloudinary library using the credentials
    cloudinary.config( 
        cloud_name = CLOUDINARY_CLOUD_NAME, 
        api_key = CLOUDINARY_API_KEY, 
        api_secret = CLOUDINARY_API_SECRET,
        secure=True
    )


# -------------------------------
# Django REST Framework
# -------------------------------
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# -------------------------------
# CORS
# -------------------------------
# Safer configuration based on DEBUG status
CORS_ALLOW_ALL_ORIGINS = DEBUG 
# Only allow specific domains in production
CORS_ALLOWED_ORIGINS = ['https://e-commerce-o7m0.onrender.com']
CSRF_TRUSTED_ORIGINS = ['https://e-commerce-o7m0.onrender.com']
CORS_ALLOW_CREDENTIALS = True


# -------------------------------
# Default primary key field
# -------------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# -------------------------------
# JWT Settings
# -------------------------------
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True, 
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# -------------------------------
# API Documentation (DRF Spectacular)
# -------------------------------
SPECTACULAR_SETTINGS = {
    'TITLE': 'E-Commerce API',
    'DESCRIPTION': 'API documentation for the Django/DRF E-Commerce Backend.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False, 
}

