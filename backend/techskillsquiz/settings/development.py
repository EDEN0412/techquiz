"""
Django開発環境設定ファイル
開発時に使用される設定を定義します
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# .env.developmentファイルを読み込み
env_path = Path(__file__).resolve().parent.parent.parent.parent / '.env.development'
load_dotenv(dotenv_path=env_path)

# 基本設定を継承
from .base import *

# 開発環境フラグの設定
IS_LOCAL_DEVELOPMENT = True

# 開発環境ではデバッグを有効化
DEBUG = True

# 開発環境ではすべてのオリジンからのCORSを許可
CORS_ALLOW_ALL_ORIGINS = True

# 開発環境でのSupabase同期は有効化
SUPABASE_AUTO_SYNC = os.environ.get("SUPABASE_AUTO_SYNC", "True").lower() in ("true", "1", "t")

# 開発環境用データベース設定
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DATABASE_NAME", "postgres"),
        "USER": os.environ.get("DATABASE_USER", "postgres"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD", "postgres"),
        "HOST": os.environ.get("DATABASE_HOST", "localhost"),
        "PORT": os.environ.get("DATABASE_PORT", "5432"),
    }
}

# 開発環境用のログ設定
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'supabase_sync.log'),
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'techskillsquiz.supabase_sync': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# 開発環境用Django Debug Toolbar設定
try:
    import debug_toolbar
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')
    INTERNAL_IPS = ['127.0.0.1']
except ImportError:
    pass 