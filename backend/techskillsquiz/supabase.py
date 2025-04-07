"""
Supabase Client Configuration

このモジュールはSupabase APIへの接続設定を管理します。
"""

import os
from supabase import create_client, Client

# 環境変数からSupabaseの接続情報を取得
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_ANON_KEY")

# クライアントインスタンスを作成
supabase: Client = None

def initialize_supabase():
    """Supabaseクライアントを初期化します"""
    global supabase
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError(
            "Supabase接続情報が設定されていません。環境変数SUPABASE_URLとSUPABASE_ANON_KEYを設定してください。"
        )
    
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase

def get_supabase_client() -> Client:
    """Supabaseクライアントのインスタンスを返します。
    まだ初期化されていない場合は初期化します。
    """
    global supabase
    if supabase is None:
        return initialize_supabase()
    return supabase 