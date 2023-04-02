"""
Django settings for api project.

Generated by "django-admin startproject" using Django 4.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.templatetags.static import static
import os
from pathlib import Path

import dj_database_url

# Build paths inside the project like this: BASE_DIR / "subdir".
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-8wyexs_^#gsu1r3#p+(@#ck^u(*vhjbj(ju8na8_kfl(b7lt@r"

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = "RENDER" not in os.environ

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGIN_REGEXES = [
    # r"^https?:\/\/(.+\.)*fiary\.app$",
]
ALLOWED_HOSTS = [
    # ".fiary.app"
]

RENDER_EXTERNAL_HOSTNAME = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

if DEBUG:
    ALLOWED_HOSTS += [
        "localhost",
        "127.0.0.1",
        ".onrender.com",
    ]

    CORS_ALLOWED_ORIGIN_REGEXES += [
        r"^http(s)?://localhost:8080$",
        r"^http(s)?://localhost:8000$",
        r"^http(s)?://127.0.0.1:8080$",
        r"^http(s)?://127.0.0.1:8000$",
    ]

# Application definition

INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "graphene_django",
    "corsheaders",
    "social_django",
    "django_filters",
    "authentication.apps.AuthenticationConfig",
    "common.apps.CommonConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "api.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "api.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        default="postgresql://postgres:postgres@localhost:5432/postgres",
        conn_max_age=600
    )
}


# GraphQL

GRAPHENE = {
    "SCHEMA": "api.schema.schema",
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
    ],
}

# User & Authentication

AUTH_USER_MODEL = "authentication.User"
SOCIAL_AUTH_USER_MODEL = "authentication.User"
SOCIAL_AUTH_JSONFIELD_ENABLED = True
SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
AUTHENTICATION_BACKENDS = (
    "social_core.backends.google.GoogleOAuth2",
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
)
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ.get("GOOGLE_OAUTH2_CLIENT_ID")
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ.get("GOOGLE_OAUTH2_SECRET")

SOCIAL_AUTH_PIPELINE = (
    "social_core.pipeline.social_auth.social_details",
    "social_core.pipeline.social_auth.social_uid",
    "social_core.pipeline.social_auth.social_user",
    "social_core.pipeline.user.get_username",
    "social_core.pipeline.social_auth.associate_by_email",
    "social_core.pipeline.user.create_user",
    "social_core.pipeline.social_auth.associate_user",
    "social_core.pipeline.social_auth.load_extra_data",
    "social_core.pipeline.user.user_details",
)


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880

UNFOLD = {
    "SITE_TITLE": "Listany Admin",
    "SITE_HEADER": "Listany Admin",
    "SITE_URL": "/",
    # "SITE_ICON": lambda request: static("logo.svg"),
    # "DASHBOARD_CALLBACK": "sample_app.dashboard_callback",
    "LOGIN": {
        "image": lambda r: static("common/images/pexels-anni-roenkae-2832382.jpg"),
        "redirect_after": lambda r: reverse_lazy("admin:index"),
    },
    "STYLES": [],
    "SCRIPTS": [],
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": False,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        # "badge": "sample_app.badge_callback",
                    },
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:authentication_user_changelist"),
                    },
                ],
            },
        ],
    },
    "TABS": [
        {
            "models": [
                "authentication.user",
                "auth.group",
                "social_django.usersocialauth",
            ],
            "items": [
                {
                    "title": _("All Users"),
                    "link": reverse_lazy("admin:authentication_user_changelist"),
                },
                {
                    "title": _("All Groups"),
                    "link": reverse_lazy("admin:auth_group_changelist"),
                },
                {
                    "title": _("All Social Accounts"),
                    "link": reverse_lazy("admin:social_django_usersocialauth_changelist"),
                },
            ],
        },
    ],
}


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
