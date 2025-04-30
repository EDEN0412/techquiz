"""
pytest設定ファイル

このファイルはpytestの実行を設定するために使用されます。
PythonPATHの設定やDjangoのセットアップ、環境変数の読み込みなど、
テスト環境のセットアップに必要な設定を行います。
"""

import os
import sys
from pathlib import Path

# プロジェクトのルートディレクトリを取得
ROOT_DIR = Path(__file__).resolve().parent

# バックエンドディレクトリをPythonPATHに追加
backend_path = ROOT_DIR / 'backend'
sys.path.insert(0, str(backend_path))

# Djangoの設定モジュールを設定
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techskillsquiz.settings.test')
os.environ.setdefault('PYTHONPATH', f"{os.environ.get('PYTHONPATH', '')}:{str(backend_path)}")

# pytestのプラグイン設定
pytest_plugins = [
    'pytest_django',
]

def pytest_configure(config):
    """pytestの設定を行います"""
    # env_filesが正しく読み込まれていない場合に備えて、.env.testを確実に読み込む
    from dotenv import load_dotenv
    env_file = ROOT_DIR / '.env.test'
    if env_file.exists():
        load_dotenv(env_file)
    
    # Djangoセットアップ
    import django
    django.setup()
    
    print("テスト環境が設定されました")
    print(f"設定モジュール: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    print(f"テスト環境フラグ: IS_TESTING={os.environ.get('IS_TESTING', 'Not set')}") 