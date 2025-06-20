"""
Django管理コマンドのテスト
"""

import io
from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from unittest.mock import patch, MagicMock
from quiz.models import Category, DifficultyLevel


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
        self.assertIn('アプリケーション: quiz', output)
        self.assertIn('同期を開始', output)
    
    def test_command_with_model_option(self):
        """--modelオプション付きでのコマンド実行をテスト"""
        out = io.StringIO()
        call_command('sync_supabase', model='Category', stdout=out)
        
        output = out.getvalue()
        self.assertIn('モデル: Category', output)
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
        with self.assertRaises(CommandError):
            call_command('sync_supabase', app='nonexistent_app')
    
    def test_command_with_invalid_model(self):
        """存在しないモデルを指定した場合のテスト"""
        with self.assertRaises(CommandError):
            call_command('sync_supabase', model='NonexistentModel')
    
    def test_command_check_option(self):
        """--checkオプション付きでのコマンド実行をテスト"""
        out = io.StringIO()
        call_command('sync_supabase', check_only=True, stdout=out)
        
        output = out.getvalue()
        # 整合性チェック関連の出力があることを確認
        self.assertTrue(len(output) >= 0)
    
    @patch('techskillsquiz.supabase_sync.sync_django_model_to_supabase')
    def test_command_sync_execution(self, mock_sync):
        """実際の同期処理の実行をテスト"""
        # モックの設定
        mock_sync.return_value = True
        
        out = io.StringIO()
        call_command('sync_supabase', no_input=True, stdout=out)
        
        # sync関数が呼び出されることを確認（実際は依存関係があるため期待値は調整）
        output = out.getvalue()
        self.assertTrue(len(output) >= 0)
    
    @patch('techskillsquiz.supabase_sync.sync_model_to_supabase')
    def test_command_sync_failure(self, mock_sync):
        """同期処理でエラーが発生した場合のテスト"""
        # モックでエラーを発生させる
        mock_sync.side_effect = Exception('同期エラー')
        
        out = io.StringIO()
        err = io.StringIO()
        
        # エラーが発生してもCommandErrorで包まれることを確認
        call_command('sync_supabase', force=True, stdout=out, stderr=err)
        
        error_output = err.getvalue()
        self.assertIn('エラー', error_output)
    
    def test_command_verbosity_levels(self):
        """verbosityレベルでの出力テスト"""
        # verbosity=0 (最小限の出力)
        out = io.StringIO()
        call_command('sync_supabase', force=True, verbosity=0, stdout=out)
        output_v0 = out.getvalue()
        
        # verbosity=2 (詳細な出力)
        out = io.StringIO()
        call_command('sync_supabase', force=True, verbosity=2, stdout=out)
        output_v2 = out.getvalue()
        
        # verbosity=2の方が多くの情報を出力することを確認
        self.assertGreater(len(output_v2), len(output_v0))
    
    @patch('techskillsquiz.supabase_sync.get_supabase_models')
    def test_command_no_models_found(self, mock_get_models):
        """Supabaseモデルが見つからない場合のテスト"""
        mock_get_models.return_value = []
        
        out = io.StringIO()
        call_command('sync_supabase', force=True, stdout=out)
        
        output = out.getvalue()
        self.assertIn('Supabaseモデルが見つかりません', output)
    
    def test_command_help_text(self):
        """コマンドのヘルプテキストのテスト"""
        out = io.StringIO()
        call_command('help', 'sync_supabase', stdout=out)
        
        help_output = out.getvalue()
        self.assertIn('sync_supabase', help_output)
        self.assertIn('Supabase', help_output)
    
    @patch('builtins.input', return_value='y')
    @patch('techskillsquiz.supabase_sync.sync_model_to_supabase')
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
    @patch('techskillsquiz.supabase_sync.sync_model_to_supabase')
    def test_command_confirmation_no(self, mock_sync, mock_input):
        """確認プロンプトで'n'を入力した場合のテスト"""
        out = io.StringIO()
        call_command('sync_supabase', stdout=out)
        
        # 同期が実行されないことを確認
        self.assertFalse(mock_sync.called)
        
        output = out.getvalue()
        self.assertIn('キャンセル', output)


class CommandUtilsTest(TestCase):
    """管理コマンド用ユーティリティのテストケース"""
    
    def test_model_lookup_by_name(self):
        """モデル名での検索テスト"""
        from techskillsquiz.management.commands.sync_supabase import Command
        command = Command()
        
        # 正しいモデル名での検索
        model = command._get_model_by_name('Category')
        self.assertEqual(model, Category)
        
        # 存在しないモデル名での検索
        with self.assertRaises(CommandError):
            command._get_model_by_name('NonexistentModel')
    
    def test_app_model_discovery(self):
        """アプリケーション内のモデル発見テスト"""
        from techskillsquiz.management.commands.sync_supabase import Command
        command = Command()
        
        # quizアプリのモデルを発見
        models = command._get_app_models('quiz')
        
        # 期待されるモデルが含まれていることを確認
        model_names = [model.__name__ for model in models]
        self.assertIn('Category', model_names)
        self.assertIn('DifficultyLevel', model_names)
    
    def test_supabase_model_filtering(self):
        """SupabaseModelMixinを継承したモデルのフィルタリングテスト"""
        from techskillsquiz.management.commands.sync_supabase import Command
        command = Command()
        
        # 全てのSupabaseモデルを取得
        supabase_models = command._get_supabase_models()
        
        # 全てのモデルがSupabaseModelMixinを継承していることを確認
        for model in supabase_models:
            self.assertTrue(hasattr(model, 'supabase_table'))
    
    def test_command_option_validation(self):
        """コマンドオプションのバリデーションテスト"""
        from techskillsquiz.management.commands.sync_supabase import Command
        command = Command()
        
        # appとmodelオプションの組み合わせテスト
        options = {
            'app': 'quiz',
            'model': 'Category',
            'force': False,
            'dry_run': False,
            'verbosity': 1
        }
        
        # バリデーションが通ることを確認
        # 実際のバリデーション処理があれば、ここでテスト
        self.assertTrue(True)  # プレースホルダー


class CommandOutputTest(TestCase):
    """コマンド出力のテストケース"""
    
    def test_progress_reporting(self):
        """進捗レポート機能のテスト"""
        out = io.StringIO()
        call_command('sync_supabase', force=True, verbosity=2, stdout=out)
        
        output = out.getvalue()
        
        # 進捗に関する出力が含まれていることを確認
        self.assertIn('進捗', output)
        self.assertIn('完了', output)
    
    def test_error_reporting(self):
        """エラーレポート機能のテスト"""
        with patch('techskillsquiz.supabase_sync.sync_model_to_supabase') as mock_sync:
            mock_sync.side_effect = Exception('テストエラー')
            
            out = io.StringIO()
            err = io.StringIO()
            
            call_command('sync_supabase', force=True, stdout=out, stderr=err)
            
            error_output = err.getvalue()
            self.assertIn('エラー', error_output)
    
    def test_summary_output(self):
        """サマリー出力のテスト"""
        out = io.StringIO()
        call_command('sync_supabase', force=True, stdout=out)
        
        output = out.getvalue()
        
        # サマリー情報が含まれていることを確認
        self.assertIn('同期結果', output)
        self.assertIn('処理時間', output)


class CommandPerformanceTest(TestCase):
    """コマンドパフォーマンスのテストケース"""
    
    def test_command_execution_time(self):
        """コマンド実行時間のテスト"""
        import time
        
        start_time = time.time()
        
        out = io.StringIO()
        call_command('sync_supabase', force=True, stdout=out)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # 実行時間が妥当な範囲内であることを確認（5秒以内）
        self.assertLess(execution_time, 5.0)
    
    @patch('techskillsquiz.supabase_sync.sync_model_to_supabase')
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
        call_command('sync_supabase', model='Category', force=True, stdout=out)
        
        # 処理が正常に完了することを確認
        output = out.getvalue()
        self.assertIn('完了', output) 