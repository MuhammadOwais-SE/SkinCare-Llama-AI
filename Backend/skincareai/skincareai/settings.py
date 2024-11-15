from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-8=y^)=+nc4ar!cyyu9x$o50y7vku!p9*07!44_c1(7$iav@oet'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'api.apps.ApiConfig',  # Your app here
    'rest_framework',
    'corsheaders',  # Make sure CORS headers are here
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # Remove CSRF middleware for API
    'django.middleware.csrf.CsrfViewMiddleware',  # Comment or remove this line
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Allow your frontend to talk to the backend
]

# CSRF trusted origins (optional but helps with security)
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',  # Add your frontend domain here
    'http://127.0.0.1:8000'  # Local development trusted origin
]

# Disable CSRF for local development
CSRF_COOKIE_SECURE = False  # This helps to disable CSRF checks for local development
CSRF_COOKIE_NAME = 'csrftoken'  # Default name for CSRF cookie (optional)

# Gemini API Key
GEMINI_API_KEY = "AIzaSyBWPFrTW4kRQK8Fel6fW5A_BOK4QTfo01w"

# Database Configuration (Ensure this is correct)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',  # Path to your SQLite database
    }
}


# Static URL
STATIC_URL = '/static/'
ROOT_URLCONF = 'skincareai.urls'
WSGI_APPLICATION = 'skincareai.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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
