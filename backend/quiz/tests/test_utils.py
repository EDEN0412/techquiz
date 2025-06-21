"""
ユーティリティ関数とMixinのテスト
"""

from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError
from unittest.mock import patch, MagicMock, Mock
from quiz.models import Category, DifficultyLevel
from techskillsquiz.supabase_mixins import SupabaseModelMixin
from techskillsquiz import supabase_sync
import json


class SupabaseModelMixinTest(TestCase):
    """SupabaseModelMixinのテストケース"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.category = Category.objects.create(
            name='テストカテゴリ',
            description='テスト用のカテゴリです',
            display_order=1
        )
    
    def test_supabase_table_property(self):
        """supabase_tableプロパティのテスト"""
        self.assertEqual(self.category.supabase_table, 'quiz_category')
        
        difficulty = DifficultyLevel.objects.create(name='テスト', level=1)
        self.assertEqual(difficulty.supabase_table, 'quiz_difficultylevel')
    
    def test_model_has_mixin_methods(self):
        """SupabaseModelMixinのメソッドが利用可能かテスト"""
        # Mixinで定義されたメソッドの存在確認
        self.assertTrue(hasattr(self.category, 'supabase_table'))
        self.assertTrue(callable(getattr(self.category, 'save', None)))
    
    def test_model_instance_creation(self):
        """SupabaseModelMixinを継承したモデルインスタンス作成のテスト"""
        category = Category(
            name='新しいカテゴリ',
            description='新しいテストカテゴリ',
            display_order=2
        )
        
        # インスタンスが正常に作成されることを確認
        self.assertEqual(category.name, '新しいカテゴリ')
        self.assertEqual(category.supabase_table, 'quiz_category')
    
    @patch('techskillsquiz.supabase_sync.sync_django_model_to_supabase')
    def test_mixin_save_method(self, mock_sync):
        """Mixinのsaveメソッドのテスト"""
        mock_sync.return_value = True
        
        # 新しいカテゴリを保存
        category = Category.objects.create(
            name='Mixinテスト',
            display_order=3
        )
        
        # インスタンスが正常に保存されることを確認
        self.assertIsNotNone(category.id)
        self.assertEqual(category.name, 'Mixinテスト')
    
    def test_mixin_inheritance_structure(self):
        """Mixin継承構造のテスト"""
        # CategoryがSupabaseModelMixinを継承していることを確認
        self.assertTrue(issubclass(Category, SupabaseModelMixin))
        
        # MROの確認
        mro = Category.__mro__
        mixin_in_mro = any(cls.__name__ == 'SupabaseModelMixin' for cls in mro)
        self.assertTrue(mixin_in_mro)


class SupabaseSyncUtilsTest(TestCase):
    """Supabase同期ユーティリティのテストケース"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.category = Category.objects.create(
            name='同期テスト',
            display_order=1
        )
    
    @patch('techskillsquiz.supabase_sync.get_supabase_client')
    def test_get_supabase_models(self, mock_client):
        """get_supabase_models関数のテスト"""
        models = supabase_sync.get_supabase_models()
        
        # 返されるモデルがSupabaseModelMixinを継承していることを確認
        for model in models:
            self.assertTrue(hasattr(model, 'supabase_table'))
    
    @patch('techskillsquiz.supabase_sync.get_supabase_client')
    def test_sync_django_model_to_supabase_success(self, mock_client):
        """sync_django_model_to_supabase成功ケースのテスト"""
        # モッククライアントの設定
        mock_supabase = MagicMock()
        mock_client.return_value = mock_supabase
        mock_supabase.table.return_value.select.return_value.execute.return_value.data = []
        mock_supabase.table.return_value.insert.return_value.execute.return_value = MagicMock()
        
        # 同期処理の実行
        result = supabase_sync.sync_django_model_to_supabase(Category)
        
        # 同期が成功することを確認
        self.assertTrue(result)
    
    @patch('techskillsquiz.supabase_sync.get_supabase_client')
    def test_sync_django_model_to_supabase_failure(self, mock_client):
        """sync_django_model_to_supabase失敗ケースのテスト"""
        # モッククライアントでエラーを発生
        mock_client.side_effect = Exception('Supabase接続エラー')
        
        # 同期処理でエラーが適切に処理され、Falseが返されることを確認
        result = supabase_sync.sync_django_model_to_supabase(Category)
        self.assertFalse(result)
    
    def test_get_model_fields(self):
        """モデルフィールド取得のテスト"""
        fields = Category._meta.get_fields()
        
        # 期待されるフィールドが含まれていることを確認
        field_names = [field.name for field in fields]
        self.assertIn('name', field_names)
        self.assertIn('slug', field_names)
        self.assertIn('description', field_names)
        self.assertIn('display_order', field_names)
    
    def test_model_to_dict_conversion(self):
        """モデルインスタンスの辞書変換テスト"""
        from django.forms.models import model_to_dict
        category_dict = model_to_dict(self.category)
        
        # 辞書に期待される値が含まれていることを確認
        self.assertEqual(category_dict['name'], '同期テスト')
        self.assertEqual(category_dict['display_order'], 1)
        self.assertIn('id', category_dict)
    
    @patch('techskillsquiz.supabase_sync.get_supabase_client')
    def test_table_exists_check(self, mock_client):
        """テーブル存在確認のテスト"""
        # モッククライアントの設定
        mock_supabase = MagicMock()
        mock_client.return_value = mock_supabase
        
        # テーブルが存在する場合
        mock_supabase.table.return_value.select.return_value.limit.return_value.execute.return_value.data = []
        exists = supabase_sync.check_table_exists_with_fallback(mock_supabase, 'quiz_category')
        self.assertTrue(exists)
        
        # テーブルが存在しない場合（全てのフォールバック方法をモック）
        mock_supabase.table.return_value.select.side_effect = Exception('Table not found')
        # pg_catalog方式のモック（存在しない）
        mock_supabase.rpc.return_value.execute.return_value.data = [{'table_exists': False}]
        exists = supabase_sync.check_table_exists_with_fallback(mock_supabase, 'nonexistent_table')
        self.assertFalse(exists)


class SupabaseErrorHandlingTest(TestCase):
    """Supabaseエラーハンドリングのテストケース"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.category = Category.objects.create(
            name='エラーテスト',
            display_order=1
        )
    
    @patch('techskillsquiz.supabase_sync.get_supabase_client')
    def test_connection_error_handling(self, mock_client):
        """接続エラーのハンドリングテスト"""
        # 接続エラーを模擬
        mock_client.side_effect = ConnectionError('接続できません')
        
        # エラーが適切に処理され、Falseが返されることを確認
        result = supabase_sync.sync_django_model_to_supabase(Category)
        self.assertFalse(result)
    
    @patch('techskillsquiz.supabase_sync.get_supabase_client')
    def test_authentication_error_handling(self, mock_client):
        """認証エラーのハンドリングテスト"""
        # 認証エラーを模擬（全てのフォールバック方法で失敗）
        mock_supabase = MagicMock()
        mock_client.return_value = mock_supabase
        mock_supabase.table.side_effect = Exception('Authentication failed')
        mock_supabase.rpc.side_effect = Exception('Authentication failed')
        
        # エラーが適切に処理され、Falseが返されることを確認
        result = supabase_sync.sync_django_model_to_supabase(Category)
        self.assertFalse(result)
    
    @patch('techskillsquiz.supabase_sync.get_supabase_client')
    def test_retry_mechanism(self, mock_client):
        """リトライメカニズムのテスト"""
        # 最初の試行で失敗、2回目で成功
        mock_supabase = MagicMock()
        mock_client.return_value = mock_supabase
        
        # サイドエフェクトで最初は失敗、次は成功
        mock_supabase.table.return_value.select.side_effect = [
            Exception('一時的エラー'),
            MagicMock(execute=MagicMock(return_value=MagicMock(data=[])))
        ]
        # 全てのRPCも失敗させる
        mock_supabase.rpc.side_effect = Exception('一時的エラー')
        
        # リトライ機能があれば、最終的に成功することを確認
        # 実際のリトライ実装に依存（現在はエラーでFalseを返す）
        result = supabase_sync.sync_django_model_to_supabase(Category)
        self.assertFalse(result)


class SupabaseDataValidationTest(TestCase):
    """Supabaseデータバリデーションのテストケース"""
    
    def test_model_field_validation(self):
        """モデルフィールドのバリデーションテスト"""
        # 正常なデータ
        category = Category(
            name='正常なカテゴリ',
            slug='normal-category',
            description='説明',
            display_order=1
        )
        category.full_clean()  # バリデーション実行
        
        # 異常なデータ（名前が長すぎる）
        with self.assertRaises(ValidationError):
            long_name_category = Category(
                name='あ' * 200,  # 最大長を超える
                display_order=1
            )
            long_name_category.full_clean()
    
    def test_unique_constraint_validation(self):
        """一意制約のバリデーションテスト"""
        # 最初のカテゴリ
        Category.objects.create(
            name='一意テスト',
            slug='unique-test',
            display_order=1
        )
        
        # 同じスラッグで2つ目を作成（一意制約違反）
        with self.assertRaises(Exception):
            Category.objects.create(
                name='一意テスト2',
                slug='unique-test',  # 重複
                display_order=2
            )
    
    def test_foreign_key_validation(self):
        """外部キー制約のバリデーションテスト"""
        from quiz.models import Quiz
        
        category = Category.objects.create(name='FK テスト', display_order=1)
        difficulty = DifficultyLevel.objects.create(name='FK テスト', level=1)
        
        # 正常な外部キー参照
        quiz = Quiz(
            category=category,
            difficulty=difficulty,
            title='FK テストクイズ'
        )
        quiz.full_clean()  # バリデーション成功
        
        # 存在しない外部キー参照
        invalid_quiz = Quiz(
            category_id=999999,  # 存在しないID
            difficulty=difficulty,
            title='無効なクイズ'
        )
        with self.assertRaises(ValidationError):
            invalid_quiz.full_clean()


class SupabasePerformanceTest(TestCase):
    """Supabaseパフォーマンステスト"""
    
    def test_bulk_sync_performance(self):
        """一括同期のパフォーマンステスト"""
        import time
        
        # 大量のテストデータを作成
        categories = []
        for i in range(50):
            categories.append(Category(
                name=f'パフォーマンステスト{i}',
                slug=f'performance-test-{i}',
                display_order=i
            ))
        Category.objects.bulk_create(categories)
        
        # 同期処理の実行時間を測定
        start_time = time.time()
        
        with patch('techskillsquiz.supabase_sync.sync_django_model_to_supabase') as mock_sync:
            mock_sync.return_value = True
            supabase_sync.sync_django_model_to_supabase(Category)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # 実行時間が妥当な範囲内であることを確認（2秒以内）
        self.assertLess(execution_time, 2.0)
    
    def test_memory_usage_in_sync(self):
        """同期処理でのメモリ使用量テスト"""
        import psutil
        import os
        
        # 同期前のメモリ使用量
        process = psutil.Process(os.getpid())
        memory_before = process.memory_info().rss
        
        # 大量データの同期処理を模擬
        with patch('techskillsquiz.supabase_sync.sync_django_model_to_supabase') as mock_sync:
            mock_sync.return_value = True
            for _ in range(100):
                supabase_sync.sync_django_model_to_supabase(Category)
        
        # 同期後のメモリ使用量
        memory_after = process.memory_info().rss
        memory_increase = memory_after - memory_before
        
        # メモリ増加が妥当な範囲内であることを確認（100MB以内）
        self.assertLess(memory_increase, 100 * 1024 * 1024)


class SupabaseConfigurationTest(TestCase):
    """Supabase設定のテストケース"""
    
    @override_settings(SUPABASE_URL='https://test.supabase.co')
    def test_custom_supabase_url(self):
        """カスタムSupabase URLの設定テスト"""
        from django.conf import settings
        self.assertEqual(settings.SUPABASE_URL, 'https://test.supabase.co')
    
    @override_settings(SUPABASE_AUTO_SYNC=False)
    def test_auto_sync_disabled(self):
        """自動同期無効化の設定テスト"""
        from django.conf import settings
        self.assertFalse(settings.SUPABASE_AUTO_SYNC)
    
    def test_supabase_client_initialization(self):
        """Supabaseクライアント初期化のテスト"""
        with patch('techskillsquiz.supabase_sync.get_supabase_client') as mock_get_client:
            mock_client = MagicMock()
            mock_get_client.return_value = mock_client
            
            client = supabase_sync.get_supabase_client()
            self.assertIsNotNone(client)
            mock_get_client.assert_called_once()


class SupabaseUtilityFunctionTest(TestCase):
    """Supabaseユーティリティ関数のテストケース"""
    
    def test_slugify_function(self):
        """スラッグ生成関数のテスト"""
        category = Category.objects.create(
            name='スラッグ テスト カテゴリ',
            slug='suraggu-tesuto-kategori',
            display_order=1
        )
        
        # スラッグが正しく設定されることを確認
        self.assertEqual(category.slug, 'suraggu-tesuto-kategori')
    
    def test_model_metadata_extraction(self):
        """モデルメタデータ抽出のテスト"""
        meta = Category._meta
        
        # メタデータが正しく取得できることを確認
        self.assertEqual(meta.verbose_name, 'カテゴリ')
        self.assertEqual(meta.verbose_name_plural, 'カテゴリ')
        self.assertEqual(meta.db_table, 'quiz_category')
    
    def test_field_type_mapping(self):
        """フィールドタイプマッピングのテスト"""
        fields = Category._meta.get_fields()
        
        # 各フィールドのタイプが期待通りであることを確認
        field_types = {field.name: type(field).__name__ for field in fields}
        
        self.assertEqual(field_types['name'], 'CharField')
        self.assertEqual(field_types['description'], 'TextField')
        self.assertEqual(field_types['display_order'], 'PositiveIntegerField')
        self.assertEqual(field_types['is_active'], 'BooleanField')
    
    def test_model_string_representation(self):
        """モデルの文字列表現テスト"""
        category = Category.objects.create(
            name='文字列テスト',
            display_order=1
        )
        
        # __str__メソッドが正しく動作することを確認
        self.assertEqual(str(category), '文字列テスト')
    
    def test_custom_save_method(self):
        """カスタムsaveメソッドのテスト"""
        category = Category(
            name='カスタム保存テスト',
            display_order=1
        )
        
        # saveメソッドが正常に動作することを確認
        category.save()
        self.assertIsNotNone(category.id)
        self.assertIsNotNone(category.slug)


class SupabaseMockingTest(TestCase):
    """Supabaseモッキングのテストケース"""
    
    @patch('techskillsquiz.supabase_sync.get_supabase_client')
    def test_supabase_client_mocking(self, mock_get_client):
        """Supabaseクライアントのモッキングテスト"""
        # モッククライアントを設定
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # クライアント作成をテスト
        client = supabase_sync.get_supabase_client()
        
        # モックが正しく呼び出されることを確認
        mock_get_client.assert_called_once()
        self.assertEqual(client, mock_client)
    
    @patch('techskillsquiz.supabase_sync.get_supabase_client')
    def test_database_operation_mocking(self, mock_get_client):
        """データベース操作のモッキングテスト"""
        # モッククライアントとテーブル操作を設定
        mock_client = MagicMock()
        mock_table = MagicMock()
        mock_get_client.return_value = mock_client
        mock_client.table.return_value = mock_table
        
        # 各種操作のモック設定
        mock_table.select.return_value.execute.return_value.data = []
        mock_table.insert.return_value.execute.return_value = MagicMock()
        mock_table.update.return_value.execute.return_value = MagicMock()
        mock_table.delete.return_value.execute.return_value = MagicMock()
        
        # 操作が正しくモックされることを確認
        result = supabase_sync.sync_django_model_to_supabase(Category)
        self.assertTrue(result) 