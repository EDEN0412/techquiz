"""
Django application configuration for Techskillsquiz project.
"""

from django.apps import AppConfig


class TechskillsquizConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'techskillsquiz'

    def ready(self):
        """
        アプリケーション起動時に実行される処理。
        Supabaseクライアントの初期化などを行います。
        """
        # Supabaseクライアントの初期化を試みる
        # デバッグモードまたは本番環境でのみ初期化
        from django.conf import settings
        if not settings.DEBUG or settings.SUPABASE_URL:
            try:
                from .supabase import initialize_supabase
                initialize_supabase()
                print("Supabaseクライアントが正常に初期化されました。")
            except Exception as e:
                print(f"Supabaseクライアントの初期化に失敗しました: {e}") 