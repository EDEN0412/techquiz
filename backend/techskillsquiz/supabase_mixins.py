"""
Supabase integration mixins for Django models.

このモジュールはDjangoモデルからSupabaseテーブルにアクセスするためのミックスインを提供します。
"""

from typing import Dict, List, Any, Optional, Union, Tuple
import logging
import time
import traceback
from functools import wraps

from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings

from .supabase import get_supabase_client

logger = logging.getLogger(__name__)

# カスタム例外クラス
class SupabaseMixinError(Exception):
    """SupabaseModelMixinの操作中のエラー"""
    pass

class SupabaseConnectionError(SupabaseMixinError):
    """Supabaseへの接続エラー"""
    pass

class SupabaseQueryError(SupabaseMixinError):
    """Supabaseへのクエリ実行中のエラー"""
    pass

class SupabaseDataError(SupabaseMixinError):
    """Supabaseのデータ操作中のエラー"""
    pass

def retry_on_error(max_retries=3, retry_delay=1, allowed_exceptions=(Exception,)):
    """
    エラー発生時に処理を再試行するデコレータ
    
    Args:
        max_retries: 最大再試行回数
        retry_delay: 再試行間の待機時間（秒）
        allowed_exceptions: 再試行対象の例外タイプのタプル
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries + 1):  # +1 は初回実行を含む
                try:
                    return func(*args, **kwargs)
                except allowed_exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        # エラー情報をログに記録
                        logger.warning(
                            f"関数 {func.__name__} の実行中にエラーが発生しました（試行 {attempt + 1}/{max_retries + 1}）: {str(e)}"
                        )
                        # 再試行前に待機
                        time.sleep(retry_delay)
                    else:
                        # 最大試行回数に達したらエラーをログに記録して再スロー
                        logger.error(
                            f"関数 {func.__name__} の実行が {max_retries + 1} 回の試行後に失敗しました: {str(e)}"
                        )
                        raise
            # 通常はここに到達しないが、念のため
            if last_exception:
                raise last_exception
        return wrapper
    return decorator

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
    
    # Supabase操作のリトライ回数
    supabase_retry_count: int = 3
    
    @classmethod
    def get_supabase_client(cls):
        """Supabaseクライアントを取得します"""
        try:
            return get_supabase_client()
        except Exception as e:
            error_details = traceback.format_exc()
            logger.error(f"Supabaseクライアントの取得に失敗しました: {str(e)}\n{error_details}")
            raise SupabaseConnectionError(f"Supabaseクライアントの取得に失敗しました: {str(e)}")
    
    @classmethod
    @retry_on_error(allowed_exceptions=(Exception,))
    def supabase_select(cls, *columns, **filters) -> List[Dict[str, Any]]:
        """
        Supabaseテーブルからデータを取得します。
        
        Args:
            columns: 取得するカラム名（省略時は全カラム）
            filters: フィルタリング条件
            
        Returns:
            取得したデータのリスト
            
        Raises:
            SupabaseQueryError: クエリの実行に失敗した場合
        """
        if cls.supabase_table is None:
            raise ValueError(f"{cls.__name__}のsupabase_tableが設定されていません")
        
        try:
            query = cls.get_supabase_client().table(cls.supabase_table).select(*columns)
            
            # フィルタの適用
            for key, value in filters.items():
                if value is not None:
                    query = query.eq(key, value)
                    
            result = query.execute()
            return result.data
            
        except Exception as e:
            error_details = traceback.format_exc()
            error_context = f"テーブル {cls.supabase_table} からのデータ取得中にエラーが発生しました"
            logger.error(f"{error_context}: {str(e)}\n{error_details}")
            raise SupabaseQueryError(f"{error_context}: {str(e)}")
    
    @classmethod
    @retry_on_error(allowed_exceptions=(Exception,))
    def supabase_get(cls, id_value, id_column='id') -> Optional[Dict[str, Any]]:
        """
        指定したIDのレコードを取得します。
        
        Args:
            id_value: 取得するレコードのID値
            id_column: IDカラム名（デフォルト: 'id'）
            
        Returns:
            取得したレコード、見つからない場合はNone
            
        Raises:
            SupabaseQueryError: クエリの実行に失敗した場合
        """
        try:
            result = cls.supabase_select(**{id_column: id_value})
            return result[0] if result else None
        except SupabaseMixinError:
            # 既知の例外は再スロー
            raise
        except Exception as e:
            error_details = traceback.format_exc()
            error_context = f"ID {id_value} のレコード取得中にエラーが発生しました"
            logger.error(f"{error_context}: {str(e)}\n{error_details}")
            raise SupabaseQueryError(f"{error_context}: {str(e)}")
    
    @classmethod
    @retry_on_error(allowed_exceptions=(Exception,))
    def supabase_insert(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        データを挿入します。
        
        Args:
            data: 挿入するデータ
            
        Returns:
            挿入されたデータ
            
        Raises:
            SupabaseDataError: データの挿入に失敗した場合
        """
        if cls.supabase_table is None:
            raise ValueError(f"{cls.__name__}のsupabase_tableが設定されていません")
        
        try:
            result = cls.get_supabase_client().table(cls.supabase_table).insert(data).execute()
            if not result.data:
                logger.warning(f"テーブル {cls.supabase_table} へのデータ挿入にレスポンスデータがありませんでした")
            return result.data[0] if result.data else None
        except Exception as e:
            error_details = traceback.format_exc()
            error_context = f"テーブル {cls.supabase_table} へのデータ挿入中にエラーが発生しました"
            logger.error(f"{error_context}: {str(e)}\n{error_details}")
            logger.debug(f"挿入しようとしたデータ: {data}")
            raise SupabaseDataError(f"{error_context}: {str(e)}")
    
    @classmethod
    @retry_on_error(allowed_exceptions=(Exception,))
    def supabase_update(cls, id_value, data: Dict[str, Any], id_column='id') -> Dict[str, Any]:
        """
        指定したIDのレコードを更新します。
        
        Args:
            id_value: 更新するレコードのID値
            data: 更新データ
            id_column: IDカラム名（デフォルト: 'id'）
            
        Returns:
            更新されたデータ
            
        Raises:
            SupabaseDataError: データの更新に失敗した場合
        """
        if cls.supabase_table is None:
            raise ValueError(f"{cls.__name__}のsupabase_tableが設定されていません")
        
        try:
            result = cls.get_supabase_client().table(cls.supabase_table).update(data).eq(id_column, id_value).execute()
            if not result.data:
                logger.warning(f"テーブル {cls.supabase_table} のID {id_value} の更新にレスポンスデータがありませんでした")
            return result.data[0] if result.data else None
        except Exception as e:
            error_details = traceback.format_exc()
            error_context = f"テーブル {cls.supabase_table} のID {id_value} の更新中にエラーが発生しました"
            logger.error(f"{error_context}: {str(e)}\n{error_details}")
            logger.debug(f"更新しようとしたデータ: {data}")
            raise SupabaseDataError(f"{error_context}: {str(e)}")
    
    @classmethod
    @retry_on_error(allowed_exceptions=(Exception,))
    def supabase_delete(cls, id_value, id_column='id') -> List[Dict[str, Any]]:
        """
        指定したIDのレコードを削除します。
        
        Args:
            id_value: 削除するレコードのID値
            id_column: IDカラム名（デフォルト: 'id'）
            
        Returns:
            削除されたレコード
            
        Raises:
            SupabaseDataError: データの削除に失敗した場合
        """
        if cls.supabase_table is None:
            raise ValueError(f"{cls.__name__}のsupabase_tableが設定されていません")
        
        try:
            result = cls.get_supabase_client().table(cls.supabase_table).delete().eq(id_column, id_value).execute()
            return result.data
        except Exception as e:
            error_details = traceback.format_exc()
            error_context = f"テーブル {cls.supabase_table} のID {id_value} の削除中にエラーが発生しました"
            logger.error(f"{error_context}: {str(e)}\n{error_details}")
            raise SupabaseDataError(f"{error_context}: {str(e)}")
    
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
        datetime型は自動的にISO形式の文字列に変換されます。
        
        Returns:
            Supabaseテーブルに保存可能なデータ辞書
        """
        data = {}
        
        try:
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
                
                # datetime型を文字列に変換
                from datetime import datetime, date
                if isinstance(field_value, (datetime, date)):
                    field_value = field_value.isoformat()
                
                # フィールド名をDBのカラム名に変換
                column_name = field.column
                data[column_name] = field_value
        except Exception as e:
            error_details = traceback.format_exc()
            logger.error(f"モデル {self.__class__.__name__} をSupabase用データに変換中にエラーが発生しました: {str(e)}\n{error_details}")
            raise
            
        return data
    
    @retry_on_error(allowed_exceptions=(Exception,))
    def sync_to_supabase(self) -> bool:
        """
        このモデルインスタンスをSupabaseと同期します。
        
        Returns:
            成功したかどうか
            
        Raises:
            SupabaseDataError: 同期中にエラーが発生した場合
        """
        if not self.supabase_table:
            error_msg = f"{self.__class__.__name__}のsupabase_tableが設定されていません"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
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
                operation = "更新"
            else:
                # 存在しなければ挿入
                result = self.__class__.supabase_insert(data)
                logger.debug(f"Supabaseテーブル {self.supabase_table} にレコードを挿入しました")
                operation = "挿入"
                
            if result is None:
                error_msg = f"Supabaseテーブル {self.supabase_table} のレコード {pk_value} の{operation}に失敗しました（レスポンスなし）"
                logger.error(error_msg)
                return False
                
            return True
            
        except (SupabaseMixinError, ValueError) as e:
            # 既知の例外は再スロー
            logger.error(f"Supabaseとの同期中に既知のエラーが発生しました: {str(e)}")
            raise
        except Exception as e:
            error_details = traceback.format_exc()
            error_context = f"Supabaseとの同期中に予期しないエラーが発生しました"
            error_msg = f"{error_context}: {str(e)}"
            logger.exception(error_msg)
            logger.debug(f"スタックトレース:\n{error_details}")
            raise SupabaseDataError(error_msg)
    
    @classmethod
    def verify_supabase_consistency(cls) -> Tuple[int, int, List[Any]]:
        """
        DjangoモデルとSupabaseテーブル間の整合性を検証します。
        
        Returns:
            (一致件数, 不一致件数, 不一致のID一覧)
        """
        if not cls.supabase_table:
            raise ValueError(f"{cls.__name__}のsupabase_tableが設定されていません")
            
        try:
            # テーブルの存在確認と必要に応じた作成
            client = cls.get_supabase_client()
            
            # ユーティリティ関数をローカルにインポート（循環インポートを回避）
            from .supabase_sync import check_table_exists_with_fallback, create_supabase_table
            
            table_exists = check_table_exists_with_fallback(client, cls.supabase_table)
            
            # テーブルが存在しない場合は作成
            if not table_exists:
                success = create_supabase_table(cls)
                if not success:
                    raise SupabaseDataError(f"テーブル {cls.supabase_table} の作成に失敗しました")
            
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
            
        except SupabaseDataError:
            # 既に適切な例外なので再スロー
            raise
        except Exception as e:
            error_details = traceback.format_exc()
            error_context = f"モデル {cls.__name__} の整合性検証中にエラーが発生しました"
            logger.error(f"{error_context}: {str(e)}\n{error_details}")
            raise SupabaseDataError(f"{error_context}: {str(e)}")
    
    @classmethod
    def fix_supabase_consistency(cls) -> Tuple[int, int, int]:
        """
        DjangoモデルとSupabaseテーブル間の整合性の問題を修正します。
        
        Returns:
            (確認済みレコード数, 追加されたレコード数, エラー数)
        """
        if not cls.supabase_table:
            raise ValueError(f"{cls.__name__}のsupabase_tableが設定されていません")
            
        try:
            # 整合性を検証
            try:
                matched_count, mismatched_count, mismatched_ids = cls.verify_supabase_consistency()
            except SupabaseDataError as e:
                logger.error(f"整合性検証中にエラーが発生しました: {str(e)}")
                # テーブルがなければ作成を試みる
                from .supabase_sync import create_supabase_table
                success = create_supabase_table(cls)
                if not success:
                    raise
                # 再検証
                matched_count, mismatched_count, mismatched_ids = 0, 0, []
            
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
                        logger.info(f"レコード {record_id} の同期に成功しました")
                    else:
                        error_count += 1
                        logger.warning(f"レコード {record_id} の同期に失敗しました（失敗レスポンス）")
                        
                except Exception as e:
                    error_details = traceback.format_exc()
                    logger.exception(f"レコード {record_id} の同期中にエラーが発生しました: {str(e)}")
                    logger.debug(f"スタックトレース:\n{error_details}")
                    error_count += 1
                    
            return matched_count, added_count, error_count
            
        except Exception as e:
            error_details = traceback.format_exc()
            error_context = f"モデル {cls.__name__} の整合性修正中にエラーが発生しました"
            logger.error(f"{error_context}: {str(e)}\n{error_details}")
            raise SupabaseDataError(f"{error_context}: {str(e)}")

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
    
    # 設定で自動同期が無効になっているか確認
    auto_sync = getattr(settings, 'SUPABASE_AUTO_SYNC', True)
    if not auto_sync:
        return
        
    try:
        # Supabaseと同期
        success = instance.sync_to_supabase()
        
        if success:
            logger.debug(f"{instance.__class__.__name__} ID:{instance.pk} をSupabaseと同期しました")
        else:
            logger.error(f"{instance.__class__.__name__} ID:{instance.pk} のSupabase同期に失敗しました")
            
    except Exception as e:
        error_details = traceback.format_exc()
        logger.exception(f"Supabase同期中に例外が発生しました: {str(e)}")
        logger.debug(f"スタックトレース:\n{error_details}")

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
    
    # 設定で自動同期が無効になっているか確認
    auto_sync = getattr(settings, 'SUPABASE_AUTO_SYNC', True)
    if not auto_sync:
        return
        
    try:
        # Supabaseからも削除
        instance.__class__.supabase_delete(instance.pk)
        logger.debug(f"{instance.__class__.__name__} ID:{instance.pk} をSupabaseから削除しました")
            
    except Exception as e:
        error_details = traceback.format_exc()
        logger.exception(f"Supabase削除中に例外が発生しました: {str(e)}")
        logger.debug(f"スタックトレース:\n{error_details}") 