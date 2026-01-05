"""
Django settings for literasi_bullying project
FINAL – Railway Production Ready
"""

from pathlib import Path
import os
import dj_database_url

# =====================================================
# BASE DIR
# =====================================================
BASE_DIR = Path(__file__).resolve().parent.parent


# =====================================================
# SECURITY
# =====================================================
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-local-only"
)

DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = [
    "literasi-bullying-production.up.railway.app",
    ".up.railway.app",
    "localhost",
    "127.0.0.1",
]

CSRF_TRUSTED_ORIGINS = [
    "https://literasi-bullying-production.up.railway.app",
    "https://*.railway.app",
]


# =====================================================
# APPLICATIONS
# =====================================================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Local apps
    "users.apps.UsersConfig",
    "laporan",
    "konten",
    "dashboard",
]


# =====================================================
# AUTH
# =====================================================
LOGIN_REDIRECT_URL = "/dashboard/home/"
LOGOUT_REDIRECT_URL = "/users/login/"


# =====================================================
# MIDDLEWARE
# =====================================================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# =====================================================
# URLS & TEMPLATES
# =====================================================
ROOT_URLCONF = "literasi_bullying.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "literasi_bullying.wsgi.application"


# =====================================================
# DATABASE
# =====================================================
# =====================================================
# DATABASE (FINAL – JANGAN PAKAI IF ELSE)
# =====================================================
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=True
    )
}



# =====================================================
# PASSWORD VALIDATION
# =====================================================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# =====================================================
# INTERNATIONALIZATION
# =====================================================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# =====================================================
# STATIC FILES (FINAL & FIXED)
# =====================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# 🔥 WAJIB PAKAI INI (JANGAN CONDITIONAL)
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


# =====================================================
# MEDIA FILES
# =====================================================
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


# =====================================================
# UPLOAD LIMIT
# =====================================================
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024


# =====================================================
# SECURITY HEADERS
# =====================================================
X_FRAME_OPTIONS = "SAMEORIGIN"


# =====================================================
# DEFAULT PK
# =====================================================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
