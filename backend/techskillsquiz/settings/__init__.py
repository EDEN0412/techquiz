"""
設定パッケージ初期化ファイル
環境変数に基づいて、適切な設定ファイルをインポートします
"""
import os
import sys

# デフォルトでは base.py からの設定を使用
from .base import *

# テスト実行中の場合
if 'test' in sys.argv or 'pytest' in sys.argv[0] or os.environ.get('DJANGO_SETTINGS_MODULE') == 'techskillsquiz.settings.test':
    from .test import *
# 開発環境の場合
elif os.environ.get('DJANGO_ENV') == 'development' or os.path.exists(os.path.join(BASE_DIR.parent.parent, '.env.development')):
    from .development import *
# 本番環境の場合
else:
    from .production import * 