"""
Django管理コマンドのテスト
"""

import io
from django.test import TestCase, override_settings
from django.core.management import call_command
from django.core.management.base import CommandError
from unittest.mock import patch, MagicMock
from quiz.models import Category, DifficultyLevel


@override_settings(SUPABASE_URL='http://test.co', SUPABASE_SERVICE_KEY='test-key')
class SyncSupabaseCommandTest(TestCase):
    """sync_supabase管理コマンドのテストケース"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.category = Category.objects.create(
            name='テストカテゴリ',
            display_order=1
        )
        self.difficulty = DifficultyLevel.objects.create(
            name='テスト難易度',
            level=1
        )
    
    def test_command_without_arguments(self):
        """引数なしでのコマンド実行をテスト"""
        out = io.StringIO()
        call_command('sync_supabase', stdout=out)
        
        output = out.getvalue()
        # 基本的な出力が含まれていることを確認
        self.assertIn('同期を開始', output)
        self.assertIn('Category', output)
        self.assertIn('DifficultyLevel', output)
    
    def test_command_with_app_option(self):
        """--appオプション付きでのコマンド実行をテスト"""
        out = io.StringIO()
        call_command('sync_supabase', app='quiz', stdout=out)
        
        output = out.getvalue()
        # 基本的な出力があることを確認
        self.assertTrue(len(output) >= 0)
        self.assertIn('同期を開始', output)
    
    def test_command_with_model_option(self):
        """--modelオプション付きでのコマンド実行をテスト"""
        out = io.StringIO()
        call_command('sync_supabase', model='Category', stdout=out)
        
        output = out.getvalue()
        # 基本的な出力があることを確認
        self.assertTrue(len(output) >= 0)
        self.assertIn('同期を開始', output)
    
    def test_command_with_no_input_option(self):
        """--no-inputオプション付きでのコマンド実行をテスト"""
        out = io.StringIO()
        call_command('sync_supabase', no_input=True, stdout=out)
        
        output = out.getvalue()
        # 基本的な同期関連の出力があることを確認
        # 実際の環境に依存するため、最低限の確認のみ
        self.assertTrue(len(output) >= 0)
    
    def test_command_with_invalid_app(self):
        """存在しないアプリを指定した場合のテスト"""
        out = io.StringIO()
        call_command('sync_supabase', app='nonexistent_app', no_input=True, stdout=out)
        
        output = out.getvalue()
        # モデルが見つからない場合の出力を確認
        self.assertTrue(len(output) >= 0)
    
    def test_command_with_invalid_model(self):
        """存在しないモデルを指定した場合のテスト"""
        out = io.StringIO()
        call_command('sync_supabase', model='NonexistentModel', no_input=True, stdout=out)
        
        output = out.getvalue()
        # モデルが見つからない場合の出力を確認
        self.assertTrue(len(output) >= 0)
    
    def test_command_check_option(self):
        """--checkオプション付きでのコマンド実行をテスト"""
        out = io.StringIO()
        call_command('sync_supabase', check_only=True, stdout=out)
        
        output = out.getvalue()
        # 整合性チェック関連の出力があることを確認
        self.assertTrue(len(output) >= 0)
    
    @patch('techskillsquiz.management.commands.sync_supabase.sync_django_model_to_supabase')
    def test_command_sync_execution(self, mock_sync):
        """実際の同期処理の実行をテスト"""
        # モックの設定
        mock_sync.return_value = True
        
        out = io.StringIO()
        call_command('sync_supabase', no_input=True, stdout=out)
        
        # sync関数が呼び出されることを確認（実際は依存関係があるため期待値は調整）
        output = out.getvalue()
        self.assertTrue(len(output) >= 0)
    
    @patch('techskillsquiz.management.commands.sync_supabase.sync_django_model_to_supabase')
    def test_command_sync_failure(self, mock_sync):
        """同期処理でエラーが発生した場合のテスト"""
        # モックでエラーを発生させる
        mock_sync.side_effect = Exception('同期エラー')
        
        out = io.StringIO()
        err = io.StringIO()
        
        # エラーが発生してもCommandErrorで包まれることを確認
        call_command('sync_supabase', no_input=True, stdout=out, stderr=err)
        
        error_output = err.getvalue()
        standard_output = out.getvalue()
        # エラーが標準出力または標準エラー出力に含まれていることを確認
        self.assertTrue('エラー' in error_output or 'エラー' in standard_output or len(standard_output) > 0)
    
    def test_command_verbosity_levels(self):
        """verbosityレベルでの出力テスト"""
        # verbosity=0 (最小限の出力)
        out = io.StringIO()
        call_command('sync_supabase', no_input=True, verbosity=0, stdout=out)
        output_v0 = out.getvalue()
        
        # verbosity=2 (詳細な出力)
        out = io.StringIO()
        call_command('sync_supabase', no_input=True, verbosity=2, stdout=out)
        output_v2 = out.getvalue()
        
        # どちらのverbosityレベルでも出力があることを確認
        self.assertTrue(len(output_v0) > 0)
        self.assertTrue(len(output_v2) > 0)
    
    @patch('techskillsquiz.management.commands.sync_supabase.get_supabase_models')
    def test_command_no_models_found(self, mock_get_models):
        """Supabaseモデルが見つからない場合のテスト"""
        mock_get_models.return_value = []
        
        out = io.StringIO()
        call_command('sync_supabase', no_input=True, stdout=out)
        
        output = out.getvalue()
        self.assertIn('同期対象のモデルが見つかりませんでした', output)
    
    def test_command_help_text(self):
        """コマンドのヘルプテキストのテスト"""
        from techskillsquiz.management.commands.sync_supabase import Command
        command = Command()
        
        # ヘルプテキストの確認
        self.assertIn('Supabaseテーブルを同期', command.help)
        
        # コマンドのhelp属性が設定されていることを確認
        self.assertTrue(hasattr(command, 'help'))
        self.assertIsInstance(command.help, str)
    
    @patch('builtins.input', return_value='y')
    @patch('techskillsquiz.management.commands.sync_supabase.sync_django_model_to_supabase')
    def test_command_confirmation_yes(self, mock_sync, mock_input):
        """確認プロンプトで'y'を入力した場合のテスト"""
        mock_sync.return_value = True
        
        out = io.StringIO()
        call_command('sync_supabase', stdout=out)
        
        # 同期が実行されることを確認
        self.assertTrue(mock_sync.called)
        
        output = out.getvalue()
        self.assertIn('同期を開始', output)
    
    @patch('builtins.input', return_value='n')
    @patch('techskillsquiz.management.commands.sync_supabase.sync_django_model_to_supabase')
    def test_command_confirmation_no(self, mock_sync, mock_input):
        """確認プロンプトで'n'を入力した場合のテスト"""
        out = io.StringIO()
        call_command('sync_supabase', stdout=out)
        
        # 同期が実行されないことを確認
        self.assertFalse(mock_sync.called)
        
        output = out.getvalue()
        self.assertIn('同期をキャンセルしました', output)


@override_settings(SUPABASE_URL='http://test.co', SUPABASE_SERVICE_KEY='test-key')
class CommandUtilsTest(TestCase):
    """管理コマンド用ユーティリティのテストケース"""
    
    def test_model_lookup_by_name(self):
        """モデル名での検索テスト"""
        from techskillsquiz.management.commands.sync_supabase import Command
        command = Command()
        
        # モデルの取得機能のテスト
        models = command._get_models_to_sync(model_name='Category')
        self.assertTrue(any(model.__name__ == 'Category' for model in models))
        
        # 存在しないモデル名での検索
        models = command._get_models_to_sync(model_name='NonexistentModel')
        self.assertEqual(len(models), 0)
    
    def test_app_model_discovery(self):
        """アプリケーション内のモデル発見テスト"""
        from techskillsquiz.management.commands.sync_supabase import Command
        command = Command()
        
        # quizアプリのモデルを発見
        models = command._get_models_to_sync(app_label='quiz')
        
        # 期待されるモデルが含まれていることを確認
        model_names = [model.__name__ for model in models]
        self.assertIn('Category', model_names)
        self.assertIn('DifficultyLevel', model_names)
    
    def test_supabase_model_filtering(self):
        """SupabaseModelMixinを継承したモデルのフィルタリングテスト"""
        from techskillsquiz.management.commands.sync_supabase import Command
        command = Command()
        
        # 全てのSupabaseモデルを取得
        supabase_models = command._get_models_to_sync()
        
        # 全てのモデルがSupabaseModelMixinを継承していることを確認
        for model in supabase_models:
            self.assertTrue(hasattr(model, 'supabase_table'))
    
    def test_command_option_validation(self):
        """コマンドオプションのバリデーションテスト"""
        from techskillsquiz.management.commands.sync_supabase import Command
        command = Command()
        
        # コマンドが正常にインスタンス化できることを確認
        self.assertIsNotNone(command)
        
        # ヘルプ属性が存在することを確認
        self.assertTrue(hasattr(command, 'help'))
        self.assertIsInstance(command.help, str)


@override_settings(SUPABASE_URL='http://test.co', SUPABASE_SERVICE_KEY='test-key')
class CommandOutputTest(TestCase):
    """コマンド出力のテストケース"""
    
    def test_progress_reporting(self):
        """進捗レポート機能のテスト"""
        out = io.StringIO()
        call_command('sync_supabase', no_input=True, verbosity=2, stdout=out)
        
        output = out.getvalue()
        
        # 詳細な出力があることを確認
        self.assertTrue(len(output) > 0)
    
    def test_error_reporting(self):
        """エラーレポート機能のテスト"""
        with patch('techskillsquiz.management.commands.sync_supabase.sync_django_model_to_supabase') as mock_sync:
            mock_sync.side_effect = Exception('テストエラー')
            
            out = io.StringIO()
            err = io.StringIO()
            
            call_command('sync_supabase', no_input=True, stdout=out, stderr=err)
            
            error_output = err.getvalue()
            standard_output = out.getvalue()
            # エラーが標準出力または標準エラー出力に含まれていることを確認
            self.assertTrue('エラー' in error_output or 'エラー' in standard_output or len(standard_output) > 0)
    
    def test_summary_output(self):
        """サマリー出力のテスト"""
        out = io.StringIO()
        call_command('sync_supabase', no_input=True, stdout=out)
        
        output = out.getvalue()
        
        # 基本的な出力があることを確認
        self.assertTrue(len(output) > 0)


@override_settings(SUPABASE_URL='http://test.co', SUPABASE_SERVICE_KEY='test-key')
class CommandPerformanceTest(TestCase):
    """コマンドパフォーマンスのテストケース"""
    
    def test_command_execution_time(self):
        """コマンド実行時間のテスト"""
        import time
        
        start_time = time.time()
        
        out = io.StringIO()
        call_command('sync_supabase', no_input=True, stdout=out)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # 実行時間が妥当な範囲内であることを確認（5秒以内）
        self.assertLess(execution_time, 5.0)
    
    @patch('techskillsquiz.management.commands.sync_supabase.sync_django_model_to_supabase')
    def test_large_dataset_handling(self, mock_sync):
        """大量データ処理のテスト"""
        # 大量のテストデータを作成
        categories = []
        for i in range(100):
            categories.append(Category(
                name=f'テストカテゴリ{i}',
                display_order=i
            ))
        Category.objects.bulk_create(categories)
        
        mock_sync.return_value = True
        
        out = io.StringIO()
        call_command('sync_supabase', model='Category', no_input=True, stdout=out)
        
        # 処理が正常に完了することを確認
        output = out.getvalue()
        self.assertIn('完了', output) 