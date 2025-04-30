"""
Django本番環境設定ファイル
本番環境時に使用される設定を定義します
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# .envファイルを読み込み
env_path = Path(__file__).resolve().parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# 基本設定を継承
from .base import *

# 本番環境フラグの設定
IS_PRODUCTION = True
IS_LOCAL_DEVELOPMENT = False

# 本番環境ではデバッグを無効化
DEBUG = False

# 本番環境では厳格なホスト制限
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# 本番環境ではCORSをより制限的に
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    os.environ.get("FRONTEND_URL", "https://techquiz.example.com"),
]

# 本番環境でのSupabase同期は適切に設定
SUPABASE_AUTO_SYNC = os.environ.get("SUPABASE_AUTO_SYNC", "False").lower() in ("true", "1", "t")

# 本番環境用データベース設定
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DATABASE_NAME"),
        "USER": os.environ.get("DATABASE_USER"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD"),
        "HOST": os.environ.get("DATABASE_HOST"),
        "PORT": os.environ.get("DATABASE_PORT", "5432"),
        "CONN_MAX_AGE": 60,  # 接続プーリングの設定
        "OPTIONS": {
            "sslmode": "require",  # SSL接続を強制
        }
    }
}

# 本番環境でのHTTPSリダイレクト
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000  # 1年間
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# 本番環境用のキャッシュ設定
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ.get("REDIS_URL", "redis://127.0.0.1:6379/1"),
    }
}

# 静的ファイルの設定（AWS S3やCloudFrontの使用を想定）
STATIC_URL = os.environ.get("STATIC_URL", "static/")
STATIC_ROOT = os.environ.get("STATIC_ROOT", os.path.join(BASE_DIR, 'staticfiles'))

# 本番環境用のログ設定（より制限的）
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django_error.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
} 