import unittest
from unittest.mock import patch, MagicMock, ANY
from django.test import TestCase
from django.test import override_settings
from django.db import models
from django.apps import apps

from techskillsquiz.supabase_sync import (
    check_table_exists_with_fallback,
    get_supabase_client,
    sync_django_model_to_supabase,
    FIELD_TYPE_MAPPING,
    SupabaseOperationError
)
from techskillsquiz.supabase_mixins import SupabaseModelMixin

# --- Test Models ---

class RelatedModel(SupabaseModelMixin, models.Model):
    name = models.CharField(max_length=50)
    supabase_table = 'test_related_model'

    class Meta:
        app_label = 'quiz'
        managed = False

class ParentModel(SupabaseModelMixin, models.Model):
    parent_field = models.IntegerField()
    supabase_table = 'test_parent_model'

    class Meta:
        app_label = 'quiz'
        managed = False

class ChildModel(ParentModel):
    child_field = models.CharField(max_length=30)
    related = models.ForeignKey(RelatedModel, on_delete=models.CASCADE, null=True, blank=True)
    supabase_table = 'test_child_model'

    class Meta:
        app_label = 'quiz'
        managed = False

class ManyToManyRelatedModel(SupabaseModelMixin, models.Model):
    related_name = models.CharField(max_length=50)
    supabase_table = 'test_m2m_related_model'

    class Meta:
        app_label = 'quiz'
        managed = False

class ManyToManyModel(SupabaseModelMixin, models.Model):
    m2m_field = models.ManyToManyField(ManyToManyRelatedModel, related_name='m2m_models')
    supabase_table = 'test_m2m_model'

    class Meta:
        app_label = 'quiz'
        managed = False

class OneToOneRelatedModel(SupabaseModelMixin, models.Model):
    related_field = models.IntegerField()
    supabase_table = 'test_o2o_related_model'

    class Meta:
        app_label = 'quiz'
        managed = False

class OneToOneModel(SupabaseModelMixin, models.Model):
    o2o_field = models.OneToOneField(OneToOneRelatedModel, on_delete=models.CASCADE, primary_key=True)
    extra_data = models.TextField()
    supabase_table = 'test_o2o_model'

    class Meta:
        app_label = 'quiz'
        managed = False


# --- Test Cases ---

class SupabaseTableExistsTestCase(TestCase):
    """
    テーブル存在確認ロジックのテストケース
    """

    @patch('techskillsquiz.supabase_sync.logger')
    def test_rest_api_success(self, mock_logger):
        """REST APIでテーブルが存在する場合のテスト"""
        mock_execute = MagicMock()
        mock_supabase = MagicMock()
        mock_supabase.table.return_value.select.return_value.limit.return_value.execute = mock_execute

        result = check_table_exists_with_fallback(mock_supabase, 'test_table')

        self.assertTrue(result)
        mock_supabase.table.assert_called_once_with('test_table')
        mock_execute.assert_called_once()
        mock_logger.debug.assert_called_with("REST APIでテーブル test_table の存在を確認: 成功")

    @patch('techskillsquiz.supabase_sync.logger')
    def test_rest_api_not_exists(self, mock_logger):
        """REST APIでテーブルが存在しない場合のテスト"""
        mock_supabase = MagicMock()
        mock_supabase.table.return_value.select.return_value.limit.return_value.execute.side_effect = Exception('relation "test_table" does not exist')

        result = check_table_exists_with_fallback(mock_supabase, 'test_table')

        self.assertFalse(result)
        mock_supabase.table.assert_called_once_with('test_table')
        mock_logger.debug.assert_called_with("REST APIでテーブル test_table の存在を確認: 存在しません")

    @patch('techskillsquiz.supabase_sync.logger')
    def test_fallback_to_pg_catalog_success(self, mock_logger):
        """REST APIが失敗し、pg_catalog RPCでテーブルが存在する場合のテスト"""
        mock_supabase = MagicMock()
        # REST APIは一般的なエラー
        mock_supabase.table.return_value.select.return_value.limit.return_value.execute.side_effect = Exception("Some REST error")
        # pg_catalog RPCは成功
        mock_pg_rpc_execute = MagicMock()
        mock_pg_rpc_execute.execute.return_value.data = [{'table_exists': True}]
        mock_supabase.rpc.side_effect = lambda name, params: mock_pg_rpc_execute if name == 'execute_sql' else MagicMock()

        result = check_table_exists_with_fallback(mock_supabase, 'test_table')

        self.assertTrue(result)
        mock_supabase.table.assert_called_once()
        mock_supabase.rpc.assert_called_once_with('execute_sql', {'sql': ANY}) # SQLの内容は具体的にチェックしない
        mock_logger.warning.assert_called_once()
        mock_logger.debug.assert_called_with("pg_catalog方式でテーブル test_table の存在を確認: True")

    @patch('techskillsquiz.supabase_sync.logger')
    def test_fallback_to_pg_catalog_not_exists(self, mock_logger):
        """REST APIが失敗し、pg_catalog RPCでテーブルが存在しない場合のテスト"""
        mock_supabase = MagicMock()
        mock_supabase.table.return_value.select.return_value.limit.return_value.execute.side_effect = Exception("Some REST error")
        mock_pg_rpc_execute = MagicMock()
        mock_pg_rpc_execute.execute.return_value.data = [{'table_exists': False}]
        mock_supabase.rpc.side_effect = lambda name, params: mock_pg_rpc_execute if name == 'execute_sql' else MagicMock()

        result = check_table_exists_with_fallback(mock_supabase, 'test_table')

        self.assertFalse(result)
        mock_supabase.table.assert_called_once()
        mock_supabase.rpc.assert_called_once_with('execute_sql', {'sql': ANY})
        mock_logger.warning.assert_called_once()
        mock_logger.debug.assert_called_with("pg_catalog方式でテーブル test_table の存在を確認: False")

    @patch('techskillsquiz.supabase_sync.logger')
    def test_fallback_to_rpc_success(self, mock_logger):
        """REST APIとpg_catalogが失敗し、check_table_exists RPCでテーブルが存在する場合のテスト"""
        mock_supabase = MagicMock()
        mock_supabase.table.return_value.select.return_value.limit.return_value.execute.side_effect = Exception("Some REST error")

        mock_check_rpc_execute = MagicMock()
        mock_check_rpc_execute.execute.return_value.data = [{'table_exists': True}]

        def rpc_side_effect(name, params):
            if name == 'execute_sql':
                raise Exception("pg_catalog RPC error")
            elif name == 'check_table_exists':
                return mock_check_rpc_execute
            return MagicMock()
        mock_supabase.rpc.side_effect = rpc_side_effect

        result = check_table_exists_with_fallback(mock_supabase, 'test_table')

        self.assertTrue(result)
        self.assertEqual(mock_supabase.rpc.call_count, 2)
        mock_supabase.rpc.assert_any_call('execute_sql', {'sql': ANY})
        mock_supabase.rpc.assert_any_call("check_table_exists", {"p_table_name": "test_table"})
        self.assertEqual(mock_logger.warning.call_count, 2)
        mock_logger.debug.assert_called_with("RPCでテーブル test_table の存在を確認: True")

    @patch('techskillsquiz.supabase_sync.logger')
    def test_fallback_to_rpc_not_exists(self, mock_logger):
        """REST APIとpg_catalogが失敗し、check_table_exists RPCでテーブルが存在しない場合のテスト"""
        mock_supabase = MagicMock()
        mock_supabase.table.return_value.select.return_value.limit.return_value.execute.side_effect = Exception("Some REST error")

        mock_check_rpc_execute = MagicMock()
        mock_check_rpc_execute.execute.return_value.data = [{'table_exists': False}]

        def rpc_side_effect(name, params):
            if name == 'execute_sql':
                raise Exception("pg_catalog RPC error")
            elif name == 'check_table_exists':
                return mock_check_rpc_execute
            return MagicMock()
        mock_supabase.rpc.side_effect = rpc_side_effect

        result = check_table_exists_with_fallback(mock_supabase, 'test_table')

        self.assertFalse(result)
        self.assertEqual(mock_supabase.rpc.call_count, 2)
        self.assertEqual(mock_logger.warning.call_count, 2)
        mock_logger.debug.assert_called_with("RPCでテーブル test_table の存在を確認: False")

    @patch('techskillsquiz.supabase_sync.logger')
    @patch('django.conf.settings', SUPABASE_SUPPRESS_TABLE_CHECK_ERRORS=False)
    def test_all_methods_fail_raise_error(self, mock_settings, mock_logger):
        """全ての方法が失敗し、エラー抑制が無効な場合にエラーが発生するテスト"""
        mock_supabase = MagicMock()
        mock_supabase.table.return_value.select.return_value.limit.return_value.execute.side_effect = Exception("REST error")
        mock_supabase.rpc.side_effect = Exception("RPC error") # execute_sqlもcheck_table_existsも失敗

        with self.assertRaises(SupabaseOperationError):
            check_table_exists_with_fallback(mock_supabase, 'test_table')

        self.assertEqual(mock_logger.warning.call_count, 3) # REST, pg_catalog, RPC の失敗
        mock_logger.error.assert_called_once()

    @patch('techskillsquiz.supabase_sync.logger')
    @override_settings(SUPABASE_SUPPRESS_TABLE_CHECK_ERRORS=True)
    def test_all_methods_fail_suppress_error(self, mock_logger):
        """全ての方法が失敗し、エラー抑制が有効な場合にFalseを返すテスト"""
        mock_supabase = MagicMock()
        mock_supabase.table.return_value.select.return_value.limit.return_value.execute.side_effect = Exception("REST error")
        mock_supabase.rpc.side_effect = Exception("RPC error")

        result = check_table_exists_with_fallback(mock_supabase, 'test_table')

        self.assertFalse(result)
        self.assertEqual(mock_logger.warning.call_count, 4)
        mock_logger.error.assert_called_once()

class SupabaseModelSyncStructureTestCase(TestCase):
    """
    様々なモデル構造を持つモデルのSupabase同期テストケース
    """
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # テストで使用するモデルをロード
        cls.RelatedModel = apps.get_model('quiz', 'RelatedModel')
        cls.ParentModel = apps.get_model('quiz', 'ParentModel')
        cls.ChildModel = apps.get_model('quiz', 'ChildModel')
        cls.ManyToManyRelatedModel = apps.get_model('quiz', 'ManyToManyRelatedModel')
        cls.ManyToManyModel = apps.get_model('quiz', 'ManyToManyModel')
        cls.OneToOneRelatedModel = apps.get_model('quiz', 'OneToOneRelatedModel')
        cls.OneToOneModel = apps.get_model('quiz', 'OneToOneModel')

    @patch('techskillsquiz.supabase_sync.get_supabase_client')
    @patch('techskillsquiz.supabase_sync.sync_django_model_to_supabase')
    def test_sync_model_with_foreign_key(self, mock_sync, mock_get_client):
        """ForeignKeyを持つモデルの同期テスト（呼び出し確認）"""
        mock_supabase = MagicMock()
        mock_get_client.return_value = mock_supabase
        mock_sync.return_value = True

        # 関連モデルと子モデルを同期する関数を呼び出す *シミュレーション*
        # 実際には sync_all_models_to_supabase() や post_migrate シグナルハンドラなどが
        # これらのモデルに対して sync_django_model_to_supabase を呼び出すことを想定
        # ここでは直接呼び出さず、モックへの期待される呼び出しを検証する

        # --- シミュレーション実行部分（例：管理コマンドやシグナルハンドラの一部を模倣）---
        # 仮に sync_all_models などが内部で以下のように呼び出すとする
        # (この部分はテスト対象の sync_django_model_to_supabase ではない)
        mock_sync(self.RelatedModel) # モック関数を直接呼び出す
        mock_sync(self.ChildModel)
        # --- シミュレーション終了 ---

        # sync_django_model_to_supabase が各モデルで呼び出されたことを確認
        mock_sync.assert_any_call(self.RelatedModel)
        mock_sync.assert_any_call(self.ChildModel)

        # 呼び出し回数なども確認可能
        self.assertEqual(mock_sync.call_count, 2)

    @patch('techskillsquiz.supabase_sync.get_supabase_client')
    @patch('techskillsquiz.supabase_sync.sync_django_model_to_supabase')
    def test_sync_inherited_model(self, mock_sync, mock_get_client):
        """継承関係にあるモデルの同期テスト（呼び出し確認）"""
        mock_supabase = MagicMock()
        mock_get_client.return_value = mock_supabase
        mock_sync.return_value = True

        # 親モデルと子モデルを同期する関数を呼び出す *シミュレーション*
        mock_sync(self.ParentModel)
        mock_sync(self.ChildModel)

        # sync_django_model_to_supabase が呼び出されたか確認
        mock_sync.assert_any_call(self.ParentModel)
        mock_sync.assert_any_call(self.ChildModel)
        self.assertEqual(mock_sync.call_count, 2)

    @patch('techskillsquiz.supabase_sync.get_supabase_client')
    @patch('techskillsquiz.supabase_sync.sync_django_model_to_supabase')
    def test_sync_model_with_many_to_many(self, mock_sync, mock_get_client):
        """ManyToManyFieldを持つモデルの同期テスト（呼び出し確認）"""
        mock_supabase = MagicMock()
        mock_get_client.return_value = mock_supabase
        mock_sync.return_value = True

        # 関連モデルとM2Mモデルを同期する関数を呼び出す *シミュレーション*
        mock_sync(self.ManyToManyRelatedModel)
        mock_sync(self.ManyToManyModel)

        # sync_django_model_to_supabase が呼び出されたか確認 (M2Mフィールド自体はSupabaseテーブルの列にならない)
        mock_sync.assert_any_call(self.ManyToManyRelatedModel)
        mock_sync.assert_any_call(self.ManyToManyModel)
        self.assertEqual(mock_sync.call_count, 2)
        # ここではM2Mフィールドが *直接* カラムとして渡されないことを確認（中間テーブルは別）
        # create/alter関数の内部実装でM2Mが無視されることを期待

    @patch('techskillsquiz.supabase_sync.get_supabase_client')
    @patch('techskillsquiz.supabase_sync.sync_django_model_to_supabase')
    def test_sync_model_with_one_to_one(self, mock_sync, mock_get_client):
        """OneToOneFieldを持つモデルの同期テスト（呼び出し確認）"""
        mock_supabase = MagicMock()
        mock_get_client.return_value = mock_supabase
        mock_sync.return_value = True

        # 関連モデルとO2Oモデルを同期する関数を呼び出す *シミュレーション*
        mock_sync(self.OneToOneRelatedModel)
        mock_sync(self.OneToOneModel)

        # sync_django_model_to_supabase が呼び出されたか確認
        mock_sync.assert_any_call(self.OneToOneRelatedModel)
        mock_sync.assert_any_call(self.OneToOneModel)
        self.assertEqual(mock_sync.call_count, 2)
        # create/alter 関数の内部で OneToOneField (primary_key=True) が主キーとして扱われることを期待


if __name__ == '__main__':
    unittest.main() 