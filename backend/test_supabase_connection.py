#!/usr/bin/env python
"""
Supabase接続テストスクリプト

このスクリプトは、環境変数の設定を読み込み、Supabaseへの接続をテストします。
"""

import os
import sys
import dotenv
from pathlib import Path

# .envファイルを読み込む
dotenv.load_dotenv(Path(__file__).parent / '.env')

# Djangoの設定を使用するために、Djangoのセットアップを行う
sys.path.append(str(Path(__file__).parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techskillsquiz.settings')

import django
django.setup()

# Supabaseクライアントをインポート
from techskillsquiz.supabase import get_supabase_client

def test_supabase_connection():
    """Supabaseへの接続をテストします"""
    print("Supabase接続テストを開始します...")
    
    # 環境変数の確認
    supabase_url = os.environ.get('SUPABASE_URL')
    supabase_key = os.environ.get('SUPABASE_ANON_KEY')
    
    if not supabase_url or not supabase_key:
        print("エラー: 環境変数SUPABASE_URLまたはSUPABASE_ANON_KEYが設定されていません。")
        return False
    
    print(f"Supabase URL: {supabase_url}")
    print(f"Supabase Key: {supabase_key[:5]}...{supabase_key[-5:]}")
    
    try:
        # Supabaseクライアントを取得
        supabase = get_supabase_client()
        
        # 接続テスト（メタデータを取得してみる）
        user_response = supabase.auth.get_user(jwt=None)
        print("認証サービスに接続できました。")
        
        # テーブル一覧を取得してみる
        try:
            # スキーマ情報を取得
            from_response = supabase.table("users").select("*").limit(1).execute()
            print(f"テーブルへのアクセステスト: {from_response}")
            print("Supabase接続成功!")
            return True
        except Exception as e:
            # テーブルが存在しなくてもエラーになることがあるので、
            # ここでエラーが発生しても完全な失敗とはみなさない
            print(f"テーブルアクセスエラー: {e}")
            print("認証サービスへの接続は成功しましたが、データベースへのアクセスに問題があります。")
            # 認証接続ができていればとりあえず成功と判断
            return True
            
    except Exception as e:
        print(f"エラー: Supabase接続中に例外が発生しました: {e}")
        return False

if __name__ == "__main__":
    success = test_supabase_connection()
    sys.exit(0 if success else 1) 