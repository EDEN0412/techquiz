"""
Supabase同期コマンド

このコマンドはDjangoモデルとSupabaseテーブルを手動で同期するための機能を提供します。
既存のSupabaseModelMixinを継承したモデルを検出し、対応するSupabaseテーブルの作成やスキーマ更新を行います。

使用例:
    python manage.py sync_supabase                # 全モデルの同期
    python manage.py sync_supabase --app=users    # 特定アプリのモデルのみ同期
    python manage.py sync_supabase --model=User   # 特定モデルのみ同期
    python manage.py sync_supabase --no-input     # 確認なしで実行
    python manage.py sync_supabase --verbose      # 詳細ログ出力
"""

import sys
import logging
from typing import List, Type, Dict, Any, Optional
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps
from django.db import models
from django.conf import settings

from techskillsquiz.supabase_sync import (
    get_supabase_models,
    sync_django_model_to_supabase,
    sync_all_models_to_supabase
)
from techskillsquiz.supabase_mixins import SupabaseModelMixin

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'DjangoモデルとSupabaseテーブルを同期します'

    def add_arguments(self, parser):
        """コマンドライン引数の設定"""
        parser.add_argument(
            '--app',
            dest='app_label',
            help='同期するアプリケーション名を指定します',
        )
        parser.add_argument(
            '--model', 
            dest='model_name',
            help='同期する特定のモデル名を指定します',
        )
        parser.add_argument(
            '--no-input',
            action='store_true',
            dest='no_input',
            default=False,
            help='確認なしで実行します',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            dest='verbose',
            default=False,
            help='詳細なログを出力します',
        )

    def handle(self, *args, **options):
        """コマンド実行時のメイン処理"""
        # オプションの取得
        app_label = options.get('app_label')
        model_name = options.get('model_name')
        no_input = options.get('no_input')
        verbose = options.get('verbose')

        # ロギングの設定
        if verbose:
            handler = logging.StreamHandler(sys.stdout)
            logger.addHandler(handler)
            logger.setLevel(logging.DEBUG)

        # Supabaseの接続情報が設定されているか確認
        if not all([settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY]):
            self.stderr.write(
                self.style.ERROR('Supabase接続情報が設定されていません。.env.developmentファイルを確認してください。')
            )
            return

        # 同期対象のモデルを取得
        models_to_sync = self._get_models_to_sync(app_label, model_name)
        
        if not models_to_sync:
            self.stdout.write(
                self.style.WARNING('同期対象のモデルが見つかりませんでした。')
            )
            return

        # 同期対象のモデル情報を表示
        self._display_models_info(models_to_sync)

        # 確認プロンプト
        if not no_input and not self._confirm_sync():
            self.stdout.write(self.style.WARNING('同期をキャンセルしました。'))
            return

        # 同期実行
        self._perform_sync(models_to_sync, verbose)

    def _get_models_to_sync(self, app_label: Optional[str] = None, model_name: Optional[str] = None) -> List[Type[SupabaseModelMixin]]:
        """同期対象のモデルを取得する"""
        # 全Supabaseモデルを取得
        all_models = get_supabase_models()

        # フィルタリング
        if app_label:
            all_models = [m for m in all_models if m._meta.app_label == app_label]

        if model_name:
            all_models = [m for m in all_models if m.__name__ == model_name]

        return all_models

    def _display_models_info(self, models: List[Type[SupabaseModelMixin]]):
        """同期対象のモデル情報を表示"""
        self.stdout.write(self.style.SUCCESS(f'以下のモデルとSupabaseテーブルを同期します（{len(models)}件）:'))
        
        for model in models:
            table_name = model._meta.db_table
            self.stdout.write(f' - {model._meta.app_label}.{model.__name__} → {table_name}')

    def _confirm_sync(self) -> bool:
        """同期実行の確認"""
        user_input = input('同期を実行しますか？ [y/N]: ').lower()
        return user_input in ('y', 'yes')

    def _perform_sync(self, models: List[Type[SupabaseModelMixin]], verbose: bool):
        """同期を実行"""
        self.stdout.write('同期を開始します...')
        
        results = {}
        
        for model in models:
            model_name = f"{model._meta.app_label}.{model.__name__}"
            table_name = model._meta.db_table
            
            self.stdout.write(f' - {model_name} の同期を実行中...')
            
            try:
                success = sync_django_model_to_supabase(model)
                results[model_name] = success
                
                if success:
                    self.stdout.write(self.style.SUCCESS(f'   ✓ {table_name} テーブルの同期に成功しました'))
                else:
                    self.stdout.write(self.style.ERROR(f'   ✗ {table_name} テーブルの同期に失敗しました'))
                    
            except Exception as e:
                results[model_name] = False
                self.stdout.write(self.style.ERROR(f'   ✗ {table_name} テーブルの同期中にエラーが発生しました: {str(e)}'))
                if verbose:
                    import traceback
                    traceback.print_exc()
        
        # 結果の集計
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)
        
        if total_count > 0:
            self.stdout.write(self.style.SUCCESS(
                f'同期が完了しました！ {success_count}/{total_count} のモデルが正常に同期されました。'
            ))
            
            # 失敗したモデルがあれば表示
            failed_models = [model for model, success in results.items() if not success]
            if failed_models:
                self.stdout.write(self.style.WARNING(f'以下のモデルの同期に失敗しました:'))
                for model in failed_models:
                    self.stdout.write(f' - {model}') 