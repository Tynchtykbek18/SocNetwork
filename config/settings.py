import os
from pathlib import Path
from environs import Env
from datetime import timedelta
from corsheaders.defaults import default_headers

BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()
env_file = os.getenv("ENV_FILE", ".env")
env.read_env(env_file)

SECRET_KEY = env.str("SECRET_KEY")

DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "daphne",
    "django.contrib.staticfiles",
    "celery",
    "drf_yasg",
    "corsheaders",
    "rest_framework",
    "channels",
    "rest_framework.authtoken",
    "apps.user.apps.UserConfig",
    "apps.post.apps.PostConfig",
    "apps.timetable.apps.TimetableConfig",
    "apps.follower.apps.FollowerConfig",
    "apps.story.apps.StoryConfig",
    "apps.chat.apps.ChatConfig",
    "apps.menu.apps.MenuConfig",
    "apps.complaint.apps.ComplaintConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
AUTH_USER_MODEL = "user.User"
WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"


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

CELERY_BEAT_SCHEDULE = {
    'update_story_statuses': {
        'task': 'apps.story.tasks.update_story_statuses',
        'schedule': timedelta(minutes=1),
    },
}

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.TokenAuthentication",
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=24),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=12),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,
    "JWT_ALLOW_REFRESH": True,
    "JWT_EXPIRATION_DELTA": timedelta(hours=24),
    "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=14),
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "api_key": {
            "type": "apiKey",
            "description": "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token",
            "in": "header",
            "name": "Authorization",
        },
    },
}


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# cors
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = ["http://localhost:3000"]
CORS_ALLOW_HEADERS = (
    *default_headers,
    "Timezone",
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "bil382",
#         "USER": "tynchtyk",
#         "PASSWORD": "tynch18",
#         "HOST": "localhost",
#         "PORT": "5432",
#     }
# }

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

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "key"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "secret"

LANGUAGE_CODE = "ru"

TIME_ZONE = "Asia/Bishkek"

USE_I18N = True

USE_TZ = True

WEBSOCKET_BASE_URL = 'http://34.125.249.56'

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
# STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env.str("EMAIL_HOST")
EMAIL_PORT = env.str("EMAIL_PORT")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS")
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL")

CELERY_BROKER_URL = env.str("REDIS_HOST")
CELERY_RESULT_BACKEND = env.str("REDIS_HOST")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DATA_UPLOAD_MAX_MEMORY_SIZE = 1024 * 1024 * 50
