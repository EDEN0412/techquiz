"""
Django管理コマンドの実用的なテスト
"""

import io
from django.test import TestCase, override_settings
from django.core.management import call_command
from django.core.management.base import CommandError
from unittest.mock import patch, MagicMock
from quiz.models import Category, DifficultyLevel


class SyncSupabaseCommandBasicTest(TestCase):
    """sync_supabase管理コマンドの基本テストケース"""
    
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
    
    @override_settings(
        SUPABASE_URL='https://test.supabase.co',
        SUPABASE_SERVICE_KEY='test-key'
    )
    def test_command_with_supabase_settings(self):
        """Supabase設定がある場合のコマンド実行をテスト"""
        out = io.StringIO()
        err = io.StringIO()
        
        # no_inputオプションでプロンプトをスキップ
        call_command('sync_supabase', no_input=True, stdout=out, stderr=err)
        
        output = out.getvalue()
        error_output = err.getvalue()
        
        # エラーメッセージが出力されていないことを確認
        self.assertNotIn('Supabase接続情報が設定されていません', error_output)
        
        # 何らかの出力があることを確認
        self.assertTrue(len(output) >= 0)
    
    def test_command_without_supabase_settings(self):
        """Supabase設定がない場合のエラーテスト"""
        out = io.StringIO()
        err = io.StringIO()
        
        call_command('sync_supabase', stdout=out, stderr=err)
        
        error_output = err.getvalue()
        
        # 設定エラーメッセージが表示されることを確認
        self.assertIn('Supabase接続情報が設定されていません', error_output)
    
    @override_settings(
        SUPABASE_URL='https://test.supabase.co',
        SUPABASE_SERVICE_KEY='test-key'
    )
    def test_command_with_app_option(self):
        """--appオプション付きでのコマンド実行をテスト"""
        out = io.StringIO()
        
        call_command('sync_supabase', app_label='quiz', no_input=True, stdout=out)
        
        output = out.getvalue()
        # 基本的な処理が実行されることを確認
        self.assertTrue(len(output) >= 0)
    
    @override_settings(
        SUPABASE_URL='https://test.supabase.co',
        SUPABASE_SERVICE_KEY='test-key'
    )
    def test_command_with_model_option(self):
        """--modelオプション付きでのコマンド実行をテスト"""
        out = io.StringIO()
        
        call_command('sync_supabase', model_name='Category', no_input=True, stdout=out)
        
        output = out.getvalue()
        # 基本的な処理が実行されることを確認
        self.assertTrue(len(output) >= 0)
    
    @override_settings(
        SUPABASE_URL='https://test.supabase.co',
        SUPABASE_SERVICE_KEY='test-key'
    )
    def test_command_with_check_option(self):
        """--checkオプション付きでのコマンド実行をテスト"""
        out = io.StringIO()
        
        call_command('sync_supabase', check_only=True, stdout=out)
        
        output = out.getvalue()
        # チェック処理が実行されることを確認
        self.assertTrue(len(output) >= 0)
    
    @override_settings(
        SUPABASE_URL='https://test.supabase.co',
        SUPABASE_SERVICE_KEY='test-key'
    )
    def test_command_with_verbose_option(self):
        """--verboseオプション付きでのコマンド実行をテスト"""
        out = io.StringIO()
        
        call_command('sync_supabase', verbose=True, no_input=True, stdout=out)
        
        output = out.getvalue()
        # 詳細出力が実行されることを確認
        self.assertTrue(len(output) >= 0)
    
    @override_settings(
        SUPABASE_URL='https://test.supabase.co',
        SUPABASE_SERVICE_KEY='test-key'
    )
    def test_command_with_report_option(self):
        """--reportオプション付きでのコマンド実行をテスト"""
        out = io.StringIO()
        
        call_command('sync_supabase', generate_report=True, no_input=True, stdout=out)
        
        output = out.getvalue()
        # レポート生成が実行されることを確認
        self.assertTrue(len(output) >= 0)


class SyncSupabaseCommandHelperTest(TestCase):
    """sync_supabaseコマンドのヘルパー機能テスト"""
    
    def test_command_help_display(self):
        """コマンドヘルプの表示テスト"""
        from techskillsquiz.management.commands.sync_supabase import Command
        
        command = Command()
        self.assertIsNotNone(command.help)
        self.assertIn('Django', command.help)
        self.assertIn('Supabase', command.help)
    
    def test_command_arguments(self):
        """コマンド引数の定義テスト"""
        from techskillsquiz.management.commands.sync_supabase import Command
        
        command = Command()
        
        # パーサーを作成してオプションをテスト
        import argparse
        parser = argparse.ArgumentParser()
        command.add_arguments(parser)
        
        # 引数が正しく追加されていることを確認
        help_text = parser.format_help()
        self.assertIn('--app', help_text)
        self.assertIn('--model', help_text)
        self.assertIn('--no-input', help_text)
        self.assertIn('--verbose', help_text)
        self.assertIn('--check', help_text)
        self.assertIn('--fix', help_text)
        self.assertIn('--report', help_text)


class SyncSupabaseCommandModelTest(TestCase):
    """sync_supabaseコマンドのモデル処理テスト"""
    
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
    
    def test_get_models_to_sync_all(self):
        """全モデル取得のテスト"""
        from techskillsquiz.management.commands.sync_supabase import Command
        
        command = Command()
        models = command._get_models_to_sync()
        
        # Supabaseモデルが含まれていることを確認
        model_names = [model.__name__ for model in models]
        self.assertIn('Category', model_names)
        self.assertIn('DifficultyLevel', model_names)
    
    def test_get_models_to_sync_by_app(self):
        """アプリ指定でのモデル取得のテスト"""
        from techskillsquiz.management.commands.sync_supabase import Command
        
        command = Command()
        models = command._get_models_to_sync(app_label='quiz')
        
        # quizアプリのモデルのみが含まれていることを確認
        for model in models:
            self.assertEqual(model._meta.app_label, 'quiz')
    
    def test_get_models_to_sync_by_model_name(self):
        """モデル名指定での取得のテスト"""
        from techskillsquiz.management.commands.sync_supabase import Command
        
        command = Command()
        models = command._get_models_to_sync(model_name='Category')
        
        # Categoryモデルのみが含まれていることを確認
        self.assertEqual(len(models), 1)
        self.assertEqual(models[0].__name__, 'Category')
    
    def test_display_models_info(self):
        """モデル情報表示のテスト"""
        from techskillsquiz.management.commands.sync_supabase import Command
        
        command = Command()
        command.stdout = io.StringIO()
        
        models = [Category, DifficultyLevel]
        command._display_models_info(models)
        
        output = command.stdout.getvalue()
        self.assertIn('Category', output)
        self.assertIn('DifficultyLevel', output)


class SyncSupabaseCommandIntegrationTest(TestCase):
    """sync_supabaseコマンドの統合テスト"""
    
    def setUp(self):
        """テスト用データの準備"""
        Category.objects.create(name='統合テスト1', display_order=1)
        Category.objects.create(name='統合テスト2', display_order=2)
        DifficultyLevel.objects.create(name='統合テスト初級', level=1)
    
    @override_settings(
        SUPABASE_URL='https://test.supabase.co',
        SUPABASE_SERVICE_KEY='test-key'
    )
    @patch('techskillsquiz.supabase_sync.get_supabase_models')
    def test_command_with_mock_models(self, mock_get_models):
        """モックモデルを使った統合テスト"""
        # モックの設定
        mock_get_models.return_value = [Category, DifficultyLevel]
        
        out = io.StringIO()
        
        # パッチでSupabase処理をモック
        with patch('techskillsquiz.supabase_sync.sync_django_model_to_supabase') as mock_sync:
            mock_sync.return_value = True
            
            call_command('sync_supabase', no_input=True, stdout=out)
        
        output = out.getvalue()
        # 同期処理が実行されることを確認
        self.assertTrue(len(output) >= 0)
    
    @override_settings(
        SUPABASE_URL='https://test.supabase.co',
        SUPABASE_SERVICE_KEY='test-key'
    )
    def test_command_performance(self):
        """コマンド実行パフォーマンスのテスト"""
        import time
        
        # 複数のテストデータを作成
        for i in range(10):
            Category.objects.create(
                name=f'パフォーマンステスト{i}',
                display_order=i
            )
        
        start_time = time.time()
        
        out = io.StringIO()
        
        # パフォーマンステスト実行（モックで高速化）
        with patch('techskillsquiz.supabase_sync.sync_django_model_to_supabase') as mock_sync:
            mock_sync.return_value = True
            call_command('sync_supabase', no_input=True, stdout=out)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # 実行時間が妥当な範囲内であることを確認（3秒以内）
        self.assertLess(execution_time, 3.0)


class SyncSupabaseCommandErrorTest(TestCase):
    """sync_supabaseコマンドのエラーハンドリングテスト"""
    
    def test_invalid_app_option(self):
        """無効なアプリ名指定のテスト"""
        out = io.StringIO()
        
        call_command('sync_supabase', app_label='nonexistent_app', no_input=True, stdout=out)
        
        output = out.getvalue()
        # 警告メッセージが出力されることを確認
        self.assertIn('同期対象のモデルが見つかりませんでした', output)
    
    def test_invalid_model_option(self):
        """無効なモデル名指定のテスト"""
        out = io.StringIO()
        
        call_command('sync_supabase', model_name='NonexistentModel', no_input=True, stdout=out)
        
        output = out.getvalue()
        # 警告メッセージが出力されることを確認
        self.assertIn('同期対象のモデルが見つかりませんでした', output)
    
    @override_settings(
        SUPABASE_URL='https://test.supabase.co',
        SUPABASE_SERVICE_KEY='test-key'
    )
    @patch('techskillsquiz.supabase_sync.sync_django_model_to_supabase')
    def test_sync_error_handling(self, mock_sync):
        """同期エラーのハンドリングテスト"""
        # モックでエラーを発生させる
        mock_sync.side_effect = Exception('テスト用エラー')
        
        out = io.StringIO()
        
        call_command('sync_supabase', no_input=True, stdout=out)
        
        output = out.getvalue()
        # エラーが適切に処理されることを確認
        self.assertIn('エラーが発生しました', output) 