"""
Supabase integration mixins for Django models.

このモジュールはDjangoモデルからSupabaseテーブルにアクセスするためのミックスインを提供します。
"""

from typing import Dict, List, Any, Optional, Union, Tuple
import logging

from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from .supabase import get_supabase_client

logger = logging.getLogger(__name__)


class SupabaseModelMixin:
    """
    DjangoモデルにSupabaseテーブルへのアクセス機能を追加するミックスイン。
    
    このミックスインを使用するには、モデルクラスで継承し、supabase_table属性を設定します。
    
    Example:
        class MyModel(models.Model, SupabaseModelMixin):
            supabase_table = 'my_table'
            name = models.CharField(max_length=100)
            
            # オプションで自動同期を設定
            supabase_auto_sync = True  # デフォルトはTrue
    """
    
    # Supabaseのテーブル名（サブクラスでオーバーライドする）
    supabase_table: str = None
    
    # モデル保存時に自動的にSupabaseと同期するかどうか
    supabase_auto_sync: bool = True
    
    @classmethod
    def get_supabase_client(cls):
        """Supabaseクライアントを取得します"""
        return get_supabase_client()
    
    @classmethod
    def supabase_select(cls, *columns, **filters) -> List[Dict[str, Any]]:
        """
        Supabaseテーブルからデータを取得します。
        
        Args:
            columns: 取得するカラム名（省略時は全カラム）
            filters: フィルタリング条件
            
        Returns:
            取得したデータのリスト
        """
        if cls.supabase_table is None:
            raise ValueError(f"{cls.__name__}のsupabase_tableが設定されていません")
        
        query = cls.get_supabase_client().table(cls.supabase_table).select(*columns)
        
        # フィルタの適用
        for key, value in filters.items():
            if value is not None:
                query = query.eq(key, value)
                
        return query.execute().data
    
    @classmethod
    def supabase_get(cls, id_value, id_column='id') -> Optional[Dict[str, Any]]:
        """
        指定したIDのレコードを取得します。
        
        Args:
            id_value: 取得するレコードのID値
            id_column: IDカラム名（デフォルト: 'id'）
            
        Returns:
            取得したレコード、見つからない場合はNone
        """
        result = cls.supabase_select(**{id_column: id_value})
        return result[0] if result else None
    
    @classmethod
    def supabase_insert(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        データを挿入します。
        
        Args:
            data: 挿入するデータ
            
        Returns:
            挿入されたデータ
        """
        if cls.supabase_table is None:
            raise ValueError(f"{cls.__name__}のsupabase_tableが設定されていません")
        
        result = cls.get_supabase_client().table(cls.supabase_table).insert(data).execute()
        return result.data[0] if result.data else None
    
    @classmethod
    def supabase_update(cls, id_value, data: Dict[str, Any], id_column='id') -> Dict[str, Any]:
        """
        指定したIDのレコードを更新します。
        
        Args:
            id_value: 更新するレコードのID値
            data: 更新データ
            id_column: IDカラム名（デフォルト: 'id'）
            
        Returns:
            更新されたデータ
        """
        if cls.supabase_table is None:
            raise ValueError(f"{cls.__name__}のsupabase_tableが設定されていません")
        
        result = cls.get_supabase_client().table(cls.supabase_table).update(data).eq(id_column, id_value).execute()
        return result.data[0] if result.data else None
    
    @classmethod
    def supabase_delete(cls, id_value, id_column='id') -> List[Dict[str, Any]]:
        """
        指定したIDのレコードを削除します。
        
        Args:
            id_value: 削除するレコードのID値
            id_column: IDカラム名（デフォルト: 'id'）
            
        Returns:
            削除されたレコード
        """
        if cls.supabase_table is None:
            raise ValueError(f"{cls.__name__}のsupabase_tableが設定されていません")
        
        result = cls.get_supabase_client().table(cls.supabase_table).delete().eq(id_column, id_value).execute()
        return result.data
    
    @classmethod
    def supabase_filter(cls, **filters) -> List[Dict[str, Any]]:
        """
        指定した条件でレコードをフィルタリングします。
        
        Args:
            filters: フィルタリング条件
            
        Returns:
            フィルタリングされたレコードのリスト
        """
        return cls.supabase_select(**filters)
    
    def to_supabase_dict(self) -> Dict[str, Any]:
        """
        モデルインスタンスをSupabase用の辞書に変換します。
        
        Returns:
            Supabaseテーブルに保存可能なデータ辞書
        """
        data = {}
        
        # モデルのフィールドをループして値を取得
        for field in self._meta.fields:
            # Many-to-Manyフィールドは別のテーブルで管理されるためスキップ
            if field.many_to_many:
                continue
                
            field_name = field.name
            field_value = getattr(self, field_name)
            
            # 外部キーの場合はIDを取得
            if field.is_relation:
                if field_value is not None:
                    related_id_field = field.related_model._meta.pk.name
                    field_value = getattr(field_value, related_id_field)
            
            # フィールド名をDBのカラム名に変換
            column_name = field.column
            data[column_name] = field_value
            
        return data
    
    def sync_to_supabase(self) -> bool:
        """
        このモデルインスタンスをSupabaseと同期します。
        
        Returns:
            成功したかどうか
        """
        if not self.supabase_table:
            logger.error(f"{self.__class__.__name__}のsupabase_tableが設定されていません")
            return False
            
        try:
            # モデルのデータをSupabase用の辞書に変換
            data = self.to_supabase_dict()
            
            # 主キーの値を取得
            pk_name = self._meta.pk.name
            pk_value = getattr(self, pk_name)
            
            # 既に存在するか確認
            existing = self.__class__.supabase_get(pk_value)
            
            if existing:
                # 存在すれば更新
                result = self.__class__.supabase_update(pk_value, data)
                logger.debug(f"Supabaseテーブル {self.supabase_table} のレコード {pk_value} を更新しました")
            else:
                # 存在しなければ挿入
                result = self.__class__.supabase_insert(data)
                logger.debug(f"Supabaseテーブル {self.supabase_table} にレコードを挿入しました")
                
            return result is not None
            
        except Exception as e:
            logger.exception(f"Supabaseとの同期中にエラーが発生しました: {str(e)}")
            return False
    
    @classmethod
    def verify_supabase_consistency(cls) -> Tuple[int, int, List[Any]]:
        """
        DjangoモデルとSupabaseテーブル間の整合性を検証します。
        
        Returns:
            (一致件数, 不一致件数, 不一致のID一覧)
        """
        if not cls.supabase_table:
            raise ValueError(f"{cls.__name__}のsupabase_tableが設定されていません")
            
        # Djangoモデルの全レコードを取得
        django_records = cls.objects.all()
        
        # Supabaseの全レコードを取得
        supabase_records = cls.supabase_select()
        
        # 主キーのフィールド名を取得
        pk_name = cls._meta.pk.name
        
        # IDでSupabaseレコードをインデックス化
        supabase_by_id = {record.get(pk_name): record for record in supabase_records}
        
        # 一致しないレコードを確認
        mismatched_ids = []
        matched_count = 0
        
        for django_record in django_records:
            record_id = getattr(django_record, pk_name)
            
            if record_id not in supabase_by_id:
                # Supabaseにレコードが存在しない
                mismatched_ids.append(record_id)
            else:
                matched_count += 1
        
        return matched_count, len(mismatched_ids), mismatched_ids
    
    @classmethod
    def fix_supabase_consistency(cls) -> Tuple[int, int, int]:
        """
        DjangoモデルとSupabaseテーブル間の整合性の問題を修正します。
        
        Returns:
            (確認済みレコード数, 追加されたレコード数, エラー数)
        """
        if not cls.supabase_table:
            raise ValueError(f"{cls.__name__}のsupabase_tableが設定されていません")
            
        # 整合性を検証
        matched_count, mismatched_count, mismatched_ids = cls.verify_supabase_consistency()
        
        # 不一致がなければ終了
        if mismatched_count == 0:
            return matched_count, 0, 0
            
        # 不一致のレコードを修正
        added_count = 0
        error_count = 0
        
        for record_id in mismatched_ids:
            try:
                # Djangoレコードを取得
                record = cls.objects.get(pk=record_id)
                
                # Supabaseに同期
                success = record.sync_to_supabase()
                
                if success:
                    added_count += 1
                else:
                    error_count += 1
                    
            except Exception as e:
                logger.exception(f"レコード {record_id} の同期中にエラーが発生しました: {str(e)}")
                error_count += 1
                
        return matched_count, added_count, error_count

# シグナルハンドラ
@receiver(post_save)
def handle_supabase_sync_on_save(sender, instance, created, **kwargs):
    """
    Djangoモデル保存時のSupabase同期ハンドラ
    """
    # SupabaseModelMixinを継承しているか確認
    if not isinstance(instance, SupabaseModelMixin):
        return
        
    # 自動同期が有効か確認
    if not getattr(instance.__class__, 'supabase_auto_sync', True):
        return
        
    # supabase_tableが設定されているか確認
    if not getattr(instance.__class__, 'supabase_table', None):
        return
        
    try:
        # Supabaseと同期
        success = instance.sync_to_supabase()
        
        if success:
            logger.debug(f"{instance.__class__.__name__} ID:{instance.pk} をSupabaseと同期しました")
        else:
            logger.error(f"{instance.__class__.__name__} ID:{instance.pk} のSupabase同期に失敗しました")
            
    except Exception as e:
        logger.exception(f"Supabase同期中に例外が発生しました: {str(e)}")

@receiver(pre_delete)
def handle_supabase_delete(sender, instance, **kwargs):
    """
    Djangoモデル削除時のSupabase同期ハンドラ
    """
    # SupabaseModelMixinを継承しているか確認
    if not isinstance(instance, SupabaseModelMixin):
        return
        
    # 自動同期が有効か確認
    if not getattr(instance.__class__, 'supabase_auto_sync', True):
        return
        
    # supabase_tableが設定されているか確認
    if not getattr(instance.__class__, 'supabase_table', None):
        return
        
    try:
        # Supabaseからも削除
        instance.__class__.supabase_delete(instance.pk)
        logger.debug(f"{instance.__class__.__name__} ID:{instance.pk} をSupabaseから削除しました")
            
    except Exception as e:
        logger.exception(f"Supabase削除中に例外が発生しました: {str(e)}") 