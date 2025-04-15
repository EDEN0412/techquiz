"""
Django application configuration for Techskillsquiz project.
"""

from django.apps import AppConfig
import sys


class TechskillsquizConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'techskillsquiz'

    def ready(self):
        """
        アプリケーション起動時に実行される処理。
        Supabaseクライアントの初期化などを行います。
        """
        print(f"TechskillsquizConfig.ready() が呼び出されました", file=sys.stderr)
        
        # モジュールの自動検出（管理コマンドなど）
        from django.utils.module_loading import autodiscover_modules
        autodiscover_modules('management')
        
        # Supabaseクライアントの初期化を試みる
        # デバッグモードまたは本番環境でのみ初期化
        from django.conf import settings
        if not settings.DEBUG or settings.SUPABASE_URL:
            try:
                from .supabase import initialize_supabase
                initialize_supabase()
                print("Supabaseクライアントが正常に初期化されました。", file=sys.stderr)
            except Exception as e:
                print(f"Supabaseクライアントの初期化に失敗しました: {e}", file=sys.stderr)
                import traceback
                traceback.print_exc()
                
        # マイグレーション後のSupabase同期ハンドラを登録
        try:
            from django.db.models.signals import post_migrate
            from .supabase_sync import post_migration_sync_handler
            
            # post_migrate信号にハンドラを接続
            post_migrate.connect(post_migration_sync_handler, sender=self)
            print("Supabase同期ハンドラが登録されました。", file=sys.stderr)
            
            # 環境変数の設定状況をログに出力
            auto_sync = getattr(settings, 'SUPABASE_AUTO_SYNC', False)
            has_connection = all([settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY])
            print(f"Supabase自動同期設定: SUPABASE_AUTO_SYNC={auto_sync}, 接続情報あり={has_connection}", file=sys.stderr)
            
            if auto_sync and not has_connection:
                print("警告: SUPABASE_AUTO_SYNCが有効ですが、接続情報が不足しています。", file=sys.stderr)
        except ImportError as e:
            print(f"Supabase同期ハンドラのインポートに失敗しました: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
        except Exception as e:
            print(f"Supabase同期ハンドラの登録に失敗しました: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc() 