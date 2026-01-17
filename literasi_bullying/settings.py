"""
Django settings for literasi_bullying project
FINAL – Railway + Cloudinary + Jazzmin (DJANGO 5 READY)
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
SECRET_KEY = os.environ.get("SECRET_KEY", "django-insecure-local-only")

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
    "jazzmin",  # ⬅️ HARUS PALING ATAS

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "cloudinary",
    "cloudinary_storage",

    # Local apps
    "users.apps.UsersConfig",
    "laporan",
    "konten",
    "dashboard",
]


# =====================================================
# AUTH
# =====================================================
LOGIN_URL = "/users/login/"
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
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        ssl_require=os.environ.get("DATABASE_SSL", "false") == "true",
    )
}
# AUTO CREATE SUPERUSER (PRODUCTION SAFE)
if os.environ.get("DJANGO_SUPERUSER_USERNAME"):
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()

        if not User.objects.filter(
            username=os.environ.get("DJANGO_SUPERUSER_USERNAME")
        ).exists():
            User.objects.create_superuser(
                username=os.environ.get("DJANGO_SUPERUSER_USERNAME"),
                email=os.environ.get("DJANGO_SUPERUSER_EMAIL"),
                password=os.environ.get("DJANGO_SUPERUSER_PASSWORD"),
            )
    except Exception:
        pass


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
LANGUAGE_CODE = "id"
TIME_ZONE = "Asia/Jakarta"
USE_I18N = True
USE_TZ = True


# =====================================================
# STATIC FILES
# =====================================================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]


# =====================================================
# STORAGE
# =====================================================
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

MEDIA_URL = "/media/"


# =====================================================
# CLOUDINARY
# =====================================================
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": os.environ.get("CLOUDINARY_CLOUD_NAME"),
    "API_KEY": os.environ.get("CLOUDINARY_API_KEY"),
    "API_SECRET": os.environ.get("CLOUDINARY_API_SECRET"),
}


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


# =====================================================
# JAZZMIN ADMIN CONFIG (🔥 TAMPILAN MODERN)
# =====================================================
JAZZMIN_SETTINGS = {
    "site_title": "Admin Literasi Bullying",
    "site_header": "Sistem Literasi & Anti-Bullying",
    "site_brand": "SMP Negeri",
    "welcome_sign": "Selamat Datang Admin",
    "copyright": "© 2026 Literasi Bullying",

    "search_model": ["auth.User", "laporan.Laporan"],

    "topmenu_links": [
        {"name": "Dashboard", "url": "/dashboard/home/", "permissions": ["auth.view_user"]},
        {"model": "auth.User"},
        {"app": "laporan"},
    ],

    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.group": "fas fa-users",

        "konten.artikel": "fas fa-newspaper",
        "konten.video": "fas fa-video",
        "konten.kuis": "fas fa-question-circle",
        "konten.pertanyaan": "fas fa-list",
        "konten.opsi": "fas fa-check-circle",

        "laporan.laporan": "fas fa-file-alt",
        "users.profile": "fas fa-id-badge",
    },

    "theme": "darkly",  # 🔥 DARK MODE
}
