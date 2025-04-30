"""
シンプルな環境設定確認用テスト
"""

import os
import pytest
from django.conf import settings

def test_django_settings():
    """Djangoの設定が正しくロードされていることを確認するテスト"""
    # 設定モジュールの確認
    assert os.environ.get('DJANGO_SETTINGS_MODULE') == 'techskillsquiz.settings.test'
    
    # テスト環境フラグの確認
    assert hasattr(settings, 'IS_TESTING')
    assert settings.IS_TESTING is True
    
    # デバッグモードがオフになっていることを確認
    assert settings.DEBUG is False
    
    # データベース設定の確認
    assert 'default' in settings.DATABASES
    
    # データベースエンジンの確認（SQLiteまたはPostgreSQL）
    db_engine = settings.DATABASES['default']['ENGINE']
    assert db_engine in ['django.db.backends.sqlite3', 'django.db.backends.postgresql']
    
    # データベース名のチェック
    db_name = settings.DATABASES['default']['NAME']
    if db_engine == 'django.db.backends.sqlite3':
        # SQLiteの場合はメモリデータベースが使われる
        assert 'memory' in db_name.lower(), f"期待: メモリデータベース, 実際: {db_name}"
    else:
        # PostgreSQLの場合はテスト用データベースが使われる
        assert db_name == 'postgres_test'
    
    print("Djangoの設定が正しくロードされました")

def test_project_structure():
    """プロジェクト構造が正しいことを確認するテスト"""
    from pathlib import Path
    
    # テストファイルの場所を確認
    test_file = Path(__file__)
    
    # techskillsquiz/testsディレクトリにあることを確認
    assert test_file.parent.name == 'tests'
    assert test_file.parent.parent.name == 'techskillsquiz'
    
    print("プロジェクト構造が正しいことを確認しました") 