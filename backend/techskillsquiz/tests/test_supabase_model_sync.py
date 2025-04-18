"""
SupabaseModelMixinの同期機能のテスト

このモジュールは、DjangoモデルとSupabaseテーブル間の同期機能をテストします。
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock, call
import django
from functools import wraps

# Djangoの設定を構成
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techskillsquiz.settings')
django.setup()

from django.test import TestCase
from django.db import models
from django.db.models.signals import post_save, pre_delete

from techskillsquiz.supabase_mixins import (
    SupabaseModelMixin, 
    SupabaseQueryError,
    SupabaseConnectionError,
    SupabaseMixinError,
    SupabaseDataError
)
from techskillsquiz.supabase_sync import (
    check_table_exists_with_fallback,
    create_supabase_table,
    SupabaseSyncError,
    SupabaseOperationError
)

# テスト用のモデルクラス
class TestModel(models.Model, SupabaseModelMixin):
    """テスト用のモデルクラス"""
    
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    # Supabaseのテーブル名を指定
    supabase_table = "test_sync_table"
    
    # このモデルは実際にはデータベースに保存されない
    class Meta:
        app_label = 'test_app'
        managed = False
    
    def __str__(self):
        return self.name

class SupabaseModelSyncTestCase(TestCase):
    """
    SupabaseModelMixinの同期機能テスト
    """
    
    def setUp(self):
        """テスト環境のセットアップ"""
        # データベースモデルの保存による自動シグナル発火を無効化
        post_save.disconnect(sender=TestModel, dispatch_uid="test_disable_post_save")
        pre_delete.disconnect(sender=TestModel, dispatch_uid="test_disable_pre_delete")
        
        # テスト用のモデルインスタンスを作成
        self.test_model = TestModel(
            id=1,
            name="テスト名前",
            description="テスト説明",
            is_active=True
        )
    
    def tearDown(self):
        """テスト環境のクリーンアップ"""
        # 必要に応じてシグナルを再接続
        pass
    
    @patch('techskillsquiz.supabase_mixins.get_supabase_client')
    def test_supabase_insert_sync(self, mock_get_client):
        """新規作成したモデルがSupabaseに正しく同期されるかテスト"""
        # モックのセットアップ
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # 既存のレコードが存在しないことをシミュレート
        mock_select = MagicMock()
        mock_select.execute.return_value.data = []
        mock_client.table.return_value.select.return_value.eq.return_value = mock_select
        
        # 挿入が成功することをシミュレート
        mock_insert = MagicMock()
        mock_insert.execute.return_value.data = [
            {"id": 1, "name": "テスト名前", "description": "テスト説明", "is_active": True}
        ]
        mock_client.table.return_value.insert.return_value = mock_insert
        
        # Supabaseへの同期を実行
        result = self.test_model.sync_to_supabase()
        
        # アサーション
        self.assertTrue(result)
        
        # テーブルが呼び出されたことを確認（回数は問わない）
        mock_client.table.assert_any_call("test_sync_table")
        
        # insertが呼び出されたことを確認
        mock_client.table.return_value.insert.assert_called_once()
        
        # 引数を確認
        args, kwargs = mock_client.table.return_value.insert.call_args
        data = args[0]
        self.assertEqual(data["name"], "テスト名前")
        self.assertEqual(data["description"], "テスト説明")
        self.assertEqual(data["is_active"], True)
    
    @patch('techskillsquiz.supabase_mixins.get_supabase_client')
    def test_supabase_update_sync(self, mock_get_client):
        """更新したモデルがSupabaseに正しく同期されるかテスト"""
        # モックのセットアップ
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # 既存レコードが見つかることをシミュレート
        mock_select = MagicMock()
        mock_select.execute.return_value.data = [
            {"id": 1, "name": "古い名前", "description": "古い説明", "is_active": True}
        ]
        mock_client.table.return_value.select.return_value.eq.return_value = mock_select
        
        # 更新が成功することをシミュレート
        mock_update = MagicMock()
        mock_update.execute.return_value.data = [
            {"id": 1, "name": "テスト名前", "description": "テスト説明", "is_active": True}
        ]
        mock_client.table.return_value.update.return_value.eq.return_value = mock_update
        
        # Supabaseへの同期を実行
        result = self.test_model.sync_to_supabase()
        
        # アサーション
        self.assertTrue(result)
        
        # テーブルが呼び出されたことを確認（回数は問わない）
        mock_client.table.assert_any_call("test_sync_table")
        
        # 更新が呼び出されたことを確認
        mock_client.table.return_value.update.assert_called_once()
        
        # 更新データを確認
        update_args, update_kwargs = mock_client.table.return_value.update.call_args
        update_data = update_args[0]
        self.assertEqual(update_data["name"], "テスト名前")
        self.assertEqual(update_data["description"], "テスト説明")
        self.assertEqual(update_data["is_active"], True)
    
    @patch('techskillsquiz.supabase_mixins.get_supabase_client')
    def test_supabase_delete_sync(self, mock_get_client):
        """モデル削除がSupabaseに正しく反映されるかテスト"""
        # モックのセットアップ
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        mock_delete = MagicMock()
        mock_delete.execute.return_value.data = [
            {"id": 1, "name": "テスト名前", "description": "テスト説明", "is_active": True}
        ]
        mock_client.table.return_value.delete.return_value.eq.return_value = mock_delete
        
        # Supabaseからの削除を実行
        result = TestModel.supabase_delete(1)
        
        # アサーション
        self.assertEqual(len(result), 1)
        mock_client.table.assert_called_once_with("test_sync_table")
        mock_client.table.return_value.delete.assert_called_once()
        mock_client.table.return_value.delete.return_value.eq.assert_called_once_with("id", 1)
    
    @patch('techskillsquiz.supabase_mixins.get_supabase_client')
    def test_supabase_sync_error_handling(self, mock_get_client):
        """同期中のエラー処理が適切に機能するかテスト"""
        # モックのセットアップ
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # 既存レコードの確認をシミュレート
        mock_select = MagicMock()
        mock_select.execute.return_value.data = []
        mock_client.table.return_value.select.return_value.eq.return_value = mock_select
        
        # 例外をスローするように設定（挿入時にエラー）
        mock_client.table.return_value.insert.side_effect = Exception("Connection error")
        
        # リトライ機能をモック
        with patch('techskillsquiz.supabase_mixins.retry_on_error') as mock_retry:
            # 実際の関数を再現するモック関数
            def fake_retry(*args, **kwargs):
                def decorator(func):
                    @wraps(func)
                    def wrapper(*func_args, **func_kwargs):
                        # 最初の呼び出しで例外を発生させる
                        raise SupabaseDataError(f"テーブル test_sync_table へのデータ挿入中にエラーが発生しました: Connection error")
                    return wrapper
                return decorator
            
            # モック関数を設定
            mock_retry.side_effect = fake_retry
            
            # 現在の実装ではSupabaseDataErrorが投げられる
            with patch('techskillsquiz.supabase_mixins.time.sleep', return_value=None):
                with self.assertRaises(SupabaseDataError):
                    self.test_model.sync_to_supabase()
    
    @patch('techskillsquiz.supabase_mixins.get_supabase_client')
    def test_verify_supabase_consistency(self, mock_get_client):
        """モデルの一貫性検証機能のテスト"""
        # モックのセットアップ
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # check_table_exists_with_fallbackの結果をモック
        with patch('techskillsquiz.supabase_sync.check_table_exists_with_fallback') as mock_check_table:
            # テーブルが存在すると返す
            mock_check_table.return_value = True
            
            # Djangoデータベースクエリ結果をモック
            mock_instance1 = MagicMock(id=1, name="名前1")
            mock_instance2 = MagicMock(id=2, name="名前2")
            
            # Djangoモデルインスタンスを準備
            with patch.object(TestModel, 'objects') as mock_objects:
                mock_objects.all.return_value = [mock_instance1, mock_instance2]
                
                # Supabaseデータをモック
                mock_supabase_data = [
                    {"id": 1, "name": "名前1"},        # 一致するレコード
                    {"id": 3, "name": "名前3"},        # Django側に存在しないレコード
                ]
                
                # モックのクエリ結果を設定
                mock_select = MagicMock()
                mock_select.execute.return_value.data = mock_supabase_data
                mock_client.table.return_value.select.return_value = mock_select
                
                # 一貫性検証を実行
                matched, mismatched, mismatched_ids = TestModel.verify_supabase_consistency()
                
                # アサーション
                self.assertEqual(matched, 1)     # 一致するレコード数
                self.assertEqual(mismatched, 1)  # Supabaseに存在しないレコード数
                self.assertEqual(mismatched_ids, [2])  # Django側にあってSupabase側にないID
                
                # テーブル存在確認が呼び出されることを確認
                mock_check_table.assert_called_once()
    
    @patch('techskillsquiz.supabase_mixins.get_supabase_client')
    @patch.object(TestModel, 'verify_supabase_consistency')
    def test_fix_supabase_consistency(self, mock_verify, mock_get_client):
        """不整合のあるデータを修正する機能のテスト"""
        # モックのセットアップ
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # 挿入が成功することをシミュレート
        mock_insert = MagicMock()
        mock_insert.execute.return_value.data = [
            {"id": 1, "name": "テスト名前", "description": "テスト説明", "is_active": True}
        ]
        mock_client.table.return_value.insert.return_value = mock_insert
        
        # selectが空のリストを返すようにシミュレート
        mock_select = MagicMock()
        mock_select.execute.return_value.data = []
        mock_client.table.return_value.select.return_value.eq.return_value = mock_select
        mock_client.table.return_value.select.return_value = mock_select
        
        # Djangoインスタンス
        def mock_sync_to_supabase():
            # 上記で設定したモックが使われるので、成功を返す
            return True
            
        mock_instance1 = MagicMock(id=1, sync_to_supabase=MagicMock(side_effect=mock_sync_to_supabase))
        mock_instance2 = MagicMock(id=2, sync_to_supabase=MagicMock(side_effect=mock_sync_to_supabase))
        
        # get()の結果をモック
        with patch.object(TestModel, 'objects') as mock_objects:
            mock_objects.get.side_effect = lambda pk: (
                mock_instance1 if pk == 1 else mock_instance2 if pk == 2 else None
            )
            
            # 不整合検出結果
            matched_count = 5    # 一致するレコード数
            mismatched_count = 2  # 一致しないレコード数
            mismatched_ids = [1, 2]  # 一致しないレコードのID
            
            # verify_supabase_consistencyの戻り値を設定
            mock_verify.return_value = (matched_count, mismatched_count, mismatched_ids)
            
            # 一貫性修正を実行
            fixed_matched, fixed_added, fixed_error = TestModel.fix_supabase_consistency()
            
            # アサーション
            self.assertEqual(fixed_matched, matched_count)  # 一致していたレコード数
            self.assertEqual(fixed_added, mismatched_count)    # 追加されたレコード数
            self.assertEqual(fixed_error, 0)    # エラー数
            
            # レコード同期が呼び出されたことを確認
            self.assertEqual(mock_objects.get.call_count, 2)
            # 各レコードがsync_to_supabase()を呼んだことを確認
            mock_instance1.sync_to_supabase.assert_called_once()
            mock_instance2.sync_to_supabase.assert_called_once()
    
    @patch.object(TestModel, 'objects')
    @patch.object(TestModel, 'get_supabase_client')
    def test_table_check_error(self, mock_get_client, mock_objects):
        """テーブル存在確認でのエラーが適切に処理されるかテスト"""
        # Djangoデータベースクエリ結果をモック
        mock_objects.all.return_value = []
        
        # Supabaseクライアント
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Supabaseデータをモック
        mock_supabase_data = []
        
        # モックのクエリ結果を設定
        mock_select = MagicMock()
        mock_select.execute.return_value.data = mock_supabase_data
        mock_client.table.return_value.select.return_value = mock_select
        
        # supabase_syncモジュールからのローカルインポートをパッチ
        import sys
        from unittest.mock import patch
        
        # check_table_exists_with_fallbackの呼び出しパッチを設定
        with patch.dict(sys.modules, {'techskillsquiz.supabase_sync': MagicMock()}):
            # モジュールのインポート属性を設定
            sys.modules['techskillsquiz.supabase_sync'].check_table_exists_with_fallback = MagicMock(
                side_effect=SupabaseDataError("Failed to check table: schema error")
            )
            
            # SupabaseDataErrorが発生することを確認
            with self.assertRaises(SupabaseDataError):
                TestModel.verify_supabase_consistency()
    
    @patch.object(TestModel, 'objects')
    @patch.object(TestModel, 'get_supabase_client')
    def test_table_creation_error(self, mock_get_client, mock_objects):
        """テーブル作成エラーが適切に処理されるかテスト"""
        # Djangoデータベースクエリ結果をモック
        mock_objects.all.return_value = []
        
        # Supabaseクライアント
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        # Supabaseデータをモック
        mock_supabase_data = []
        
        # モックのクエリ結果を設定
        mock_select = MagicMock()
        mock_select.execute.return_value.data = mock_supabase_data
        mock_client.table.return_value.select.return_value = mock_select
        
        # supabase_syncモジュールからのローカルインポートをパッチ
        import sys
        from unittest.mock import patch
        
        # check_table_exists_with_fallbackとcreate_supabase_tableの呼び出しパッチを設定
        with patch.dict(sys.modules, {'techskillsquiz.supabase_sync': MagicMock()}):
            # モジュールのインポート属性を設定
            check_mock = MagicMock(return_value=False)
            create_mock = MagicMock(side_effect=SupabaseDataError("Failed to create table: permission denied"))
            
            sys.modules['techskillsquiz.supabase_sync'].check_table_exists_with_fallback = check_mock
            sys.modules['techskillsquiz.supabase_sync'].create_supabase_table = create_mock
            
            # SupabaseDataErrorが発生することを確認
            with self.assertRaises(SupabaseDataError):
                TestModel.verify_supabase_consistency()
    
    @patch('techskillsquiz.supabase_mixins.get_supabase_client')
    def test_connection_error(self, mock_get_client):
        """Supabase接続エラーが適切に処理されるかテスト"""
        # 接続エラーをシミュレート
        mock_get_client.side_effect = Exception("Supabase connection refused")
        
        # 接続エラーが発生した場合、SupabaseConnectionErrorが発生することを確認
        with self.assertRaises(SupabaseConnectionError):
            TestModel.get_supabase_client()
    
    @patch('techskillsquiz.supabase_mixins.get_supabase_client')
    def test_query_error_select(self, mock_get_client):
        """クエリ実行エラー（SELECT）が適切に処理されるかテスト"""
        # モックのセットアップ
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # セレクトクエリエラーをシミュレート
        mock_select = MagicMock()
        mock_select.execute.side_effect = Exception("Database query error: permission denied")
        mock_client.table.return_value.select.return_value = mock_select
        
        # クエリエラーが発生した場合、SupabaseQueryErrorが発生することを確認
        with self.assertRaises(SupabaseQueryError):
            TestModel.supabase_select()
    
    @patch('techskillsquiz.supabase_mixins.get_supabase_client')
    def test_query_error_insert(self, mock_get_client):
        """クエリ実行エラー（INSERT）が適切に処理されるかテスト"""
        # モックのセットアップ
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # 既存のレコードが存在しないことをシミュレート（正常）
        mock_select = MagicMock()
        mock_select.execute.return_value.data = []
        mock_client.table.return_value.select.return_value.eq.return_value = mock_select
        
        # 挿入エラーをシミュレート
        mock_client.table.return_value.insert.side_effect = Exception("Database insert error: constraint violation")
        
        # 挿入エラーが発生した場合、SupabaseDataErrorが発生することを確認
        with patch('techskillsquiz.supabase_mixins.time.sleep', return_value=None):  # リトライのsleepをスキップ
            with self.assertRaises(SupabaseDataError):
                self.test_model.sync_to_supabase()
    
    @patch('techskillsquiz.supabase_mixins.get_supabase_client')
    def test_query_error_update(self, mock_get_client):
        """クエリ実行エラー（UPDATE）が適切に処理されるかテスト"""
        # モックのセットアップ
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # 既存レコードが見つかることをシミュレート（正常）
        mock_select = MagicMock()
        mock_select.execute.return_value.data = [
            {"id": 1, "name": "古い名前", "description": "古い説明", "is_active": True}
        ]
        mock_client.table.return_value.select.return_value.eq.return_value = mock_select
        
        # 更新エラーをシミュレート
        mock_client.table.return_value.update.side_effect = Exception("Database update error: deadlock detected")
        
        # 更新エラーが発生した場合、SupabaseDataErrorが発生することを確認
        with patch('techskillsquiz.supabase_mixins.time.sleep', return_value=None):  # リトライのsleepをスキップ
            with self.assertRaises(SupabaseDataError):
                self.test_model.sync_to_supabase()
    
    @patch('techskillsquiz.supabase_mixins.get_supabase_client')
    def test_query_error_delete(self, mock_get_client):
        """クエリ実行エラー（DELETE）が適切に処理されるかテスト"""
        # モックのセットアップ
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # 削除エラーをシミュレート
        mock_client.table.return_value.delete.side_effect = Exception("Database delete error: foreign key constraint")
        
        # 削除エラーが発生した場合、SupabaseDataErrorが発生することを確認
        with patch('techskillsquiz.supabase_mixins.time.sleep', return_value=None):  # リトライのsleepをスキップ
            with self.assertRaises(SupabaseDataError):
                TestModel.supabase_delete(1)
    
    @patch('techskillsquiz.supabase_mixins.get_supabase_client')
    def test_network_timeout_error(self, mock_get_client):
        """ネットワークタイムアウトエラーが適切に処理されるかテスト"""
        # モックのセットアップ
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # タイムアウトエラーをシミュレート
        mock_select = MagicMock()
        mock_select.execute.side_effect = Exception("Network timeout error")
        mock_client.table.return_value.select.return_value = mock_select
        
        # タイムアウトエラーが発生した場合、SupabaseQueryErrorが発生し、リトライが行われることを確認
        with patch('techskillsquiz.supabase_mixins.time.sleep') as mock_sleep:
            with self.assertRaises(SupabaseQueryError):
                TestModel.supabase_select()
            
            # リトライが行われたことを確認
            self.assertGreaterEqual(mock_sleep.call_count, 1)
    
    @patch('techskillsquiz.supabase_mixins.get_supabase_client')
    def test_invalid_credentials_error(self, mock_get_client):
        """無効な認証情報エラーが適切に処理されるかテスト"""
        # モックのセットアップ
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # 認証エラーをシミュレート
        mock_select = MagicMock()
        mock_select.execute.side_effect = Exception("JWT invalid or expired")
        mock_client.table.return_value.select.return_value = mock_select
        
        # 認証エラーが発生した場合、SupabaseQueryErrorが発生することを確認
        with self.assertRaises(SupabaseQueryError):
            TestModel.supabase_select()
    
    @patch('techskillsquiz.supabase_mixins.get_supabase_client')
    def test_rate_limit_error(self, mock_get_client):
        """レート制限エラーが適切に処理されるかテスト"""
        # モックのセットアップ
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client
        
        # レート制限エラーをシミュレート
        mock_select = MagicMock()
        mock_select.execute.side_effect = Exception("Too many requests: rate limit exceeded")
        mock_client.table.return_value.select.return_value = mock_select
        
        # レート制限エラーが発生した場合、SupabaseQueryErrorが発生し、リトライが行われることを確認
        with patch('techskillsquiz.supabase_mixins.time.sleep') as mock_sleep:
            with self.assertRaises(SupabaseQueryError):
                TestModel.supabase_select()
            
            # リトライが行われたことを確認
            self.assertGreaterEqual(mock_sleep.call_count, 1)

if __name__ == '__main__':
    unittest.main() 