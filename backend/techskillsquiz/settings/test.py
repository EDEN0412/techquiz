"""
Djangoテスト環境設定ファイル
テスト実行時に使用される設定を定義します
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# .env.testファイルを読み込み
env_path = Path(__file__).resolve().parent.parent.parent.parent / '.env.test'
load_dotenv(dotenv_path=env_path)

# 基本設定を継承
from .base import *

# テスト環境フラグの設定
IS_TESTING = True

# テスト環境ではデバッグを無効化
DEBUG = False

# テスト環境での許可ホスト設定
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '[::1]',  # IPv6 localhost
    '*',      # テスト環境では全てのホストを許可（CI/CD環境用）
]

# テスト環境ではCORSをより制限的に
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://localhost:3000",  # フロントエンドプレビュー用ポート
]

# テスト環境でのSupabase同期は無効化
SUPABASE_AUTO_SYNC = False

# テスト環境用データベース設定
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DATABASE_NAME", "postgres_test"),
        "USER": os.environ.get("DATABASE_USER", "postgres"),
        "PASSWORD": os.environ.get("DATABASE_PASSWORD", "postgres"),
        "HOST": os.environ.get("DATABASE_HOST", "localhost"),
        "PORT": os.environ.get("DATABASE_PORT", "5432"),
    }
}

# メモリDBを使用可能な場合は使用する設定
if os.environ.get("USE_IN_MEMORY_DB_IF_POSSIBLE", "False").lower() in ("true", "1", "t"):
    try:
        import sqlite3
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": ":memory:",
                "TEST": {
                    "NAME": ":memory:",
                }
            }
        }
    except ImportError:
        # SQLite3が使用できない場合は上記のPostgreSQLの設定を使用
        pass

# テスト用のキャッシュ設定
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# テスト用のメディアファイル設定
MEDIA_ROOT = os.path.join(BASE_DIR, 'test_media')
MEDIA_URL = '/test-media/'

# テスト実行時の高速化のための設定
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# よりコンパクトなテストログ
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

# テスト用クライアント設定
TEST_RUNNER = os.environ.get('TEST_RUNNER', 'django.test.runner.DiscoverRunner')

# テストカバレッジのしきい値
TEST_COVERAGE_THRESHOLD = int(os.environ.get('TEST_COVERAGE_THRESHOLD', 80)) 