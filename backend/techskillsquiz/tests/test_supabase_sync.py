import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.db import models

from techskillsquiz.supabase_sync import check_table_exists_with_fallback

class SupabaseTableExistsTestCase(TestCase):
    """
    テーブル存在確認ロジックのテストケース
    """
    
    @patch('techskillsquiz.supabase_sync.logger')
    def test_table_exists_rpc_method_success(self, mock_logger):
        """RPCメソッドでテーブルが存在する場合のテスト"""
        # RPCの実行結果をモック
        mock_rpc = MagicMock()
        mock_rpc.execute.return_value.data = [{'table_exists': True}]
        
        # Supabaseクライアントをモック
        mock_supabase = MagicMock()
        mock_supabase.rpc.return_value = mock_rpc
        
        # テスト実行
        result = check_table_exists_with_fallback(mock_supabase, 'test_table')
        
        # アサーション
        self.assertTrue(result)
        mock_supabase.rpc.assert_called_once_with("check_table_exists", {"p_table_name": "test_table"})
        mock_logger.debug.assert_called_once()
    
    @patch('techskillsquiz.supabase_sync.logger')
    def test_table_not_exists_rpc_method_success(self, mock_logger):
        """RPCメソッドでテーブルが存在しない場合のテスト"""
        # RPCの実行結果をモック
        mock_rpc = MagicMock()
        mock_rpc.execute.return_value.data = [{'table_exists': False}]
        
        # Supabaseクライアントをモック
        mock_supabase = MagicMock()
        mock_supabase.rpc.return_value = mock_rpc
        
        # テスト実行
        result = check_table_exists_with_fallback(mock_supabase, 'test_table')
        
        # アサーション
        self.assertFalse(result)
        mock_supabase.rpc.assert_called_once_with("check_table_exists", {"p_table_name": "test_table"})
        mock_logger.debug.assert_called_once()
    
    @patch('techskillsquiz.supabase_sync.logger')
    def test_fallback_to_select_method_success(self, mock_logger):
        """RPCメソッドが失敗し、SELECTメソッドでテーブルが存在する場合のテスト"""
        # RPCが例外をスロー
        mock_rpc = MagicMock()
        mock_rpc.execute.side_effect = Exception("RPC failed")
        
        # SELECT実行結果をモック
        mock_select = MagicMock()
        mock_limit = MagicMock()
        mock_limit.execute.return_value = MagicMock()
        mock_select.limit.return_value = mock_limit
        
        # Supabaseクライアントをモック
        mock_supabase = MagicMock()
        mock_supabase.rpc.return_value = mock_rpc
        mock_supabase.table.return_value.select.return_value = mock_limit
        
        # テスト実行
        result = check_table_exists_with_fallback(mock_supabase, 'test_table')
        
        # アサーション
        self.assertTrue(result)
        mock_supabase.rpc.assert_called_once()
        mock_supabase.table.assert_called_once_with('test_table')
        mock_logger.warning.assert_called_once()
        mock_logger.debug.assert_called_once_with("SELECT方式でテーブル test_table の存在を確認: 成功")
    
    @patch('techskillsquiz.supabase_sync.logger')
    def test_fallback_to_select_method_table_not_exists(self, mock_logger):
        """RPCメソッドが失敗し、SELECTメソッドでテーブルが存在しない場合のテスト"""
        # RPCが例外をスロー
        mock_rpc = MagicMock()
        mock_rpc.execute.side_effect = Exception("RPC failed")
        
        # SELECTが「テーブルが存在しない」例外をスロー
        mock_supabase = MagicMock()
        mock_supabase.rpc.return_value = mock_rpc
        mock_supabase.table.return_value.select.return_value.limit.side_effect = Exception("relation \"test_table\" does not exist")
        
        # テスト実行
        result = check_table_exists_with_fallback(mock_supabase, 'test_table')
        
        # アサーション
        self.assertFalse(result)
        mock_supabase.rpc.assert_called_once()
        mock_logger.warning.assert_called()
    
    @patch('techskillsquiz.supabase_sync.logger')
    def test_fallback_to_pg_tables_method_success(self, mock_logger):
        """RPCとSELECTが失敗し、pg_tablesメソッドでテーブルが存在する場合のテスト"""
        # RPCが例外をスロー
        mock_rpc_check = MagicMock()
        mock_rpc_check.execute.side_effect = Exception("RPC failed")
        
        # SELECTが別の例外をスロー
        mock_select = MagicMock()
        mock_select.side_effect = Exception("Permission denied")
        
        # pg_tables RPC結果をモック
        mock_rpc_execute = MagicMock()
        mock_rpc_execute.execute.return_value.data = [{'table_exists': True}]
        
        # Supabaseクライアントをモック
        mock_supabase = MagicMock()
        mock_supabase.rpc.side_effect = [mock_rpc_check, mock_rpc_execute]
        mock_supabase.table.return_value.select.return_value.limit = mock_select
        
        # テスト実行
        result = check_table_exists_with_fallback(mock_supabase, 'test_table')
        
        # アサーション
        self.assertTrue(result)
        self.assertEqual(mock_supabase.rpc.call_count, 2)
        mock_logger.warning.assert_called()
    
    @patch('techskillsquiz.supabase_sync.logger')
    def test_all_methods_fail(self, mock_logger):
        """全ての方法が失敗した場合のテスト"""
        # 全てのメソッドで例外をスロー
        mock_supabase = MagicMock()
        mock_supabase.rpc.side_effect = Exception("RPC failed")
        mock_supabase.table.return_value.select.return_value.limit.side_effect = Exception("SELECT failed")
        
        # テスト実行
        result = check_table_exists_with_fallback(mock_supabase, 'test_table')
        
        # アサーション
        self.assertFalse(result)
        mock_logger.error.assert_called_once()

if __name__ == '__main__':
    unittest.main() 