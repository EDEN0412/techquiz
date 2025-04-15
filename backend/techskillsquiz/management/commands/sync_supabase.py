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
    python manage.py sync_supabase --check        # 整合性チェックのみ実行
    python manage.py sync_supabase --check --fix  # 不整合を自動修正
    python manage.py sync_supabase --report       # 詳細レポート生成
"""

import sys
import logging
import django
from typing import List, Type, Dict, Any, Optional, Tuple
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
        parser.add_argument(
            '--check',
            action='store_true',
            dest='check_only',
            default=False,
            help='整合性チェックのみを実行し、同期は行いません',
        )
        parser.add_argument(
            '--fix',
            action='store_true',
            dest='fix_consistency',
            default=False,
            help='不整合が見つかった場合に自動的に修復します',
        )
        parser.add_argument(
            '--report',
            action='store_true',
            dest='generate_report',
            default=False,
            help='同期結果の詳細レポートを生成します',
        )

    def handle(self, *args, **options):
        """コマンド実行時のメイン処理"""
        # オプションの取得
        app_label = options.get('app_label')
        model_name = options.get('model_name')
        no_input = options.get('no_input')
        verbose = options.get('verbose')
        check_only = options.get('check_only')
        fix_consistency = options.get('fix_consistency')
        generate_report = options.get('generate_report')

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

        # 整合性チェックモードの場合
        if check_only:
            self._check_consistency(models_to_sync, fix_consistency, verbose)
            return

        # 確認プロンプト
        if not no_input and not self._confirm_sync():
            self.stdout.write(self.style.WARNING('同期をキャンセルしました。'))
            return

        # 同期実行
        results = self._perform_sync(models_to_sync, verbose)
        
        # レポート生成
        if generate_report:
            self._generate_report(results, models_to_sync)

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
        import time
        
        # 処理時間計測開始
        start_time = time.time()
        
        self.stdout.write(self.style.SUCCESS('同期を開始します...'))
        
        results = {}
        total_count = len(models)
        
        for i, model in enumerate(models, 1):
            model_name = f"{model._meta.app_label}.{model.__name__}"
            table_name = model._meta.db_table
            
            self.stdout.write(f'[{i}/{total_count}] {model_name} の同期を実行中...')
            
            try:
                # 処理時間計測
                model_start_time = time.time()
                
                # モデルのフィールド情報を表示（詳細モード）
                if verbose:
                    self.stdout.write('  フィールド情報:')
                    for field in model._meta.fields:
                        field_type = field.__class__.__name__
                        nullable = 'NULL' if field.null else 'NOT NULL'
                        pk = 'PRIMARY KEY' if field.primary_key else ''
                        self.stdout.write(f'    - {field.name} ({field_type}): {nullable} {pk}')
                
                # 同期実行
                success = sync_django_model_to_supabase(model)
                results[model_name] = success
                
                # 処理時間計算
                model_time = time.time() - model_start_time
                
                if success:
                    self.stdout.write(self.style.SUCCESS(f'   ✓ {table_name} テーブルの同期に成功しました ({model_time:.2f}秒)'))
                else:
                    self.stdout.write(self.style.ERROR(f'   ✗ {table_name} テーブルの同期に失敗しました ({model_time:.2f}秒)'))
                    
            except Exception as e:
                results[model_name] = False
                self.stdout.write(self.style.ERROR(f'   ✗ {table_name} テーブルの同期中にエラーが発生しました: {str(e)}'))
                if verbose:
                    import traceback
                    self.stdout.write(self.style.ERROR('詳細なエラー情報:'))
                    traceback.print_exc()
        
        # 総処理時間
        total_time = time.time() - start_time
        
        # 結果の集計
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)
        
        if total_count > 0:
            self.stdout.write(self.style.SUCCESS(
                f'同期が完了しました！ {success_count}/{total_count} のモデルが正常に同期されました。(合計処理時間: {total_time:.2f}秒)'
            ))
            
            # 失敗したモデルがあれば表示
            failed_models = [model for model, success in results.items() if not success]
            if failed_models:
                self.stdout.write(self.style.WARNING(f'以下のモデルの同期に失敗しました:'))
                for model in failed_models:
                    self.stdout.write(self.style.ERROR(f' - {model}'))
                
                # トラブルシューティング情報
                self.stdout.write(self.style.WARNING('\nトラブルシューティング:'))
                self.stdout.write(' - Supabase接続情報が正しく設定されているか確認してください')
                self.stdout.write(' - モデルのsupabase_table属性が正しく設定されているか確認してください')
                self.stdout.write(' - --verboseオプションを付けて実行すると詳細なログが表示されます')
        
        return results

    def _check_consistency(self, models: List[Type[SupabaseModelMixin]], fix: bool, verbose: bool):
        """
        DjangoモデルとSupabaseテーブル間の整合性をチェックします
        """
        self.stdout.write(self.style.SUCCESS('整合性チェックを開始します...'))
        
        results = {}
        
        for model in models:
            model_name = f"{model._meta.app_label}.{model.__name__}"
            table_name = model._meta.db_table
            
            self.stdout.write(f' - {model_name} の整合性チェックを実行中...')
            
            try:
                matched, mismatched, mismatched_ids = model.verify_supabase_consistency()
                
                if mismatched == 0:
                    self.stdout.write(self.style.SUCCESS(f'   ✓ {table_name} テーブルは整合性が保たれています ({matched}件)'))
                    results[model_name] = {'status': 'ok', 'matched': matched, 'mismatched': 0, 'fixed': 0}
                else:
                    self.stdout.write(self.style.WARNING(
                        f'   ! {table_name} テーブルに不整合があります ({mismatched}/{matched + mismatched}件)'
                    ))
                    
                    if verbose:
                        self.stdout.write('   不整合のID:')
                        for id_value in mismatched_ids:
                            self.stdout.write(f'     - {id_value}')
                    
                    # 修正モードの場合
                    if fix:
                        self.stdout.write('   不整合を修正中...')
                        matched_count, added_count, error_count = model.fix_supabase_consistency()
                        
                        if error_count == 0:
                            self.stdout.write(self.style.SUCCESS(f'   ✓ 修正完了: {added_count}件追加'))
                            results[model_name] = {'status': 'fixed', 'matched': matched_count, 'mismatched': mismatched, 'fixed': added_count}
                        else:
                            self.stdout.write(self.style.ERROR(f'   ✗ 修正中にエラー: {error_count}件のエラー, {added_count}件は追加成功'))
                            results[model_name] = {'status': 'error', 'matched': matched_count, 'mismatched': mismatched, 'fixed': added_count, 'errors': error_count}
                    else:
                        results[model_name] = {'status': 'mismatch', 'matched': matched, 'mismatched': mismatched}
                        self.stdout.write(self.style.WARNING('   修正するには --fix オプションを付けて実行してください'))
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'   ✗ 整合性チェック中にエラーが発生しました: {str(e)}'))
                results[model_name] = {'status': 'error', 'error': str(e)}
                if verbose:
                    import traceback
                    traceback.print_exc()
        
        # 結果の集計
        ok_count = sum(1 for data in results.values() if data.get('status') == 'ok')
        fixed_count = sum(1 for data in results.values() if data.get('status') == 'fixed')
        mismatch_count = sum(1 for data in results.values() if data.get('status') == 'mismatch')
        error_count = sum(1 for data in results.values() if data.get('status') == 'error')
        
        self.stdout.write('\n整合性チェック結果:')
        self.stdout.write(f' - 整合性が保たれているモデル: {ok_count}件')
        
        if fixed_count > 0:
            self.stdout.write(self.style.SUCCESS(f' - 修正されたモデル: {fixed_count}件'))
            
        if mismatch_count > 0:
            self.stdout.write(self.style.WARNING(f' - 未修正の不整合モデル: {mismatch_count}件'))
            
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f' - エラーが発生したモデル: {error_count}件'))
            
        if mismatch_count > 0 and not fix:
            self.stdout.write('\n不整合を修正するには、--fix オプションを付けて再実行してください:')
            self.stdout.write('  python manage.py sync_supabase --check --fix')

    def _generate_report(self, results, models):
        """
        同期結果の詳細レポートを生成します
        """
        import time
        from datetime import datetime
        
        # レポートファイル名
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = f"supabase_sync_report_{timestamp}.txt"
        
        self.stdout.write(f'\n同期レポートを生成中: {report_file}')
        
        with open(report_file, 'w') as f:
            f.write(f"# Supabase同期レポート\n")
            f.write(f"生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("## 環境情報\n")
            f.write(f"Django バージョン: {django.get_version()}\n")
            f.write(f"Supabase URL: {settings.SUPABASE_URL}\n")
            f.write(f"自動同期設定: {settings.SUPABASE_AUTO_SYNC}\n\n")
            
            f.write("## 同期対象モデル\n")
            for model in models:
                f.write(f"- {model._meta.app_label}.{model.__name__} → {model._meta.db_table}\n")
            
            f.write("\n## 同期結果\n")
            for model_name, result in results.items():
                status = result.get('status', '不明')
                status_label = {
                    'ok': '成功',
                    'error': 'エラー',
                    'fixed': '修正済み',
                    'mismatch': '不整合',
                }.get(status, status)
                
                f.write(f"### {model_name}\n")
                f.write(f"状態: {status_label}\n")
                
                if 'matched' in result:
                    f.write(f"一致レコード数: {result['matched']}\n")
                
                if 'mismatched' in result:
                    f.write(f"不整合レコード数: {result['mismatched']}\n")
                
                if 'fixed' in result:
                    f.write(f"修正されたレコード数: {result['fixed']}\n")
                
                if 'errors' in result:
                    f.write(f"エラー数: {result['errors']}\n")
                
                if 'error' in result:
                    f.write(f"エラー詳細: {result['error']}\n")
                
                if 'time' in result:
                    f.write(f"処理時間: {result['time']:.2f}秒\n")
                
                f.write("\n")
            
            f.write("## まとめ\n")
            success_count = sum(1 for r in results.values() if r.get('status') in ('ok', 'fixed'))
            error_count = sum(1 for r in results.values() if r.get('status') == 'error')
            mismatch_count = sum(1 for r in results.values() if r.get('status') == 'mismatch')
            
            f.write(f"- 成功/修正済み: {success_count}件\n")
            f.write(f"- エラー: {error_count}件\n")
            f.write(f"- 未修正の不整合: {mismatch_count}件\n")
        
        self.stdout.write(self.style.SUCCESS(f'レポートが生成されました: {report_file}')) 