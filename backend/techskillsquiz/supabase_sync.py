"""
Supabase Sync Utilities

このモジュールはDjangoモデルとSupabaseテーブルの同期に関するユーティリティ関数を提供します。
マイグレーション後にDjangoモデルの変更をSupabaseテーブルに反映するための機能を含みます。
"""

import logging
from typing import Type, Dict, Any, List, Optional, Tuple, Set, Union
import inspect
import json
import traceback
from django.db import models
from django.apps import apps
from django.db.models.fields import Field
from django.db.models.fields.related import RelatedField
from django.conf import settings

from .supabase import get_supabase_client
from .supabase_mixins import SupabaseModelMixin

logger = logging.getLogger(__name__)

# SupabaseSync固有のエラークラス
class SupabaseSyncError(Exception):
    """Supabase同期処理中のエラーを表す基本例外クラス"""
    pass

class SupabaseConnectionError(SupabaseSyncError):
    """Supabaseとの接続に関するエラー"""
    pass

class SupabaseSchemaError(SupabaseSyncError):
    """テーブルスキーマに関するエラー"""
    pass

class SupabaseOperationError(SupabaseSyncError):
    """Supabase操作（クエリ実行など）に関するエラー"""
    pass

class SupabaseDataError(SupabaseSyncError):
    """データの互換性や整合性に関するエラー"""
    pass

# エラー情報収集とロギングのためのユーティリティ関数
def log_error_details(e: Exception, context: str, extra_info: Dict[str, Any] = None) -> str:
    """
    例外の詳細情報をログに記録し、エラーメッセージを返します。
    
    Args:
        e: 発生した例外
        context: エラーが発生したコンテキスト情報
        extra_info: 追加の情報辞書
        
    Returns:
        詳細なエラーメッセージ
    """
    # スタックトレースの取得
    tb_str = traceback.format_exc()
    
    # 詳細なエラー情報を構築
    error_type = type(e).__name__
    error_message = str(e)
    
    # 基本メッセージの構築
    detail_message = f"{context}: {error_type} - {error_message}"
    
    # 追加情報があれば追加
    if extra_info:
        info_str = ", ".join(f"{k}={v}" for k, v in extra_info.items())
        detail_message += f" [{info_str}]"
    
    # ログに記録
    logger.error(detail_message)
    logger.debug(f"スタックトレース:\n{tb_str}")
    
    return detail_message

# Djangoフィールドタイプとそれに対応するPostgreSQLタイプのマッピング
FIELD_TYPE_MAPPING = {
    'AutoField': 'bigint',
    'BigAutoField': 'bigint',
    'BigIntegerField': 'bigint',
    'BinaryField': 'bytea',
    'BooleanField': 'boolean',
    'CharField': 'varchar',
    'DateField': 'date',
    'DateTimeField': 'timestamp with time zone',
    'DecimalField': 'numeric',
    'DurationField': 'interval',
    'EmailField': 'varchar',
    'FileField': 'varchar',
    'FilePathField': 'varchar',
    'FloatField': 'double precision',
    'ImageField': 'varchar',
    'IntegerField': 'integer',
    'JSONField': 'jsonb',
    'NullBooleanField': 'boolean',
    'PositiveIntegerField': 'integer',
    'PositiveSmallIntegerField': 'smallint',
    'SlugField': 'varchar',
    'SmallIntegerField': 'smallint',
    'TextField': 'text',
    'TimeField': 'time',
    'URLField': 'varchar',
    'UUIDField': 'uuid',
    # 関連フィールド
    'ForeignKey': 'bigint',
    'OneToOneField': 'bigint',
    'ManyToManyField': None,  # これは別テーブルとして扱う
}

def get_supabase_models() -> List[Type[SupabaseModelMixin]]:
    """
    プロジェクト内のSupabaseModelMixinを継承したモデルを全て取得します。
    
    Returns:
        SupabaseModelMixinを継承したモデルのリスト
    """
    import sys
    supabase_models = []
    
    # 全アプリケーションのモデルを調べる
    for app_config in apps.get_app_configs():
        print(f"アプリケーション確認: {app_config.name}", file=sys.stderr)
        for model in app_config.get_models():
            print(f"  モデル確認: {model.__name__}", file=sys.stderr)
            
            # SupabaseModelMixinを継承しているか確認
            is_supabase_model = False
            try:
                is_supabase_model = issubclass(model, SupabaseModelMixin)
                if is_supabase_model:
                    print(f"    SupabaseModelMixinを継承: {model.__name__}", file=sys.stderr)
                    if hasattr(model, 'supabase_table') and model.supabase_table:
                        print(f"    supabase_table設定あり: {model.supabase_table}", file=sys.stderr)
                        supabase_models.append(model)
                    else:
                        print(f"    supabase_table設定なし: {model.__name__}", file=sys.stderr)
            except (TypeError, AttributeError) as e:
                error_msg = log_error_details(e, f"モデル継承チェック中にエラー発生: {model.__name__}")
                print(f"    継承チェックエラー: {error_msg}", file=sys.stderr)
                
    print(f"Supabaseモデル検索結果: {len(supabase_models)}件", file=sys.stderr)
    return supabase_models

def get_django_field_type(field: Field) -> Tuple[str, Dict[str, Any]]:
    """
    Djangoフィールドから対応するPostgreSQLのデータ型と属性を取得します。
    
    Args:
        field: Djangoのフィールドオブジェクト
        
    Returns:
        (PostgreSQLデータ型, 追加属性の辞書)
    """
    field_type = field.__class__.__name__
    attrs = {}
    
    # 基本的なフィールドタイプのマッピング
    pg_type = FIELD_TYPE_MAPPING.get(field_type)
    
    # 特殊なフィールド属性の処理
    if field_type == 'CharField' or field_type == 'TextField':
        if hasattr(field, 'max_length') and field.max_length:
            attrs['max_length'] = field.max_length
            if field_type == 'CharField':
                pg_type = f"varchar({field.max_length})"
    
    elif field_type == 'DecimalField':
        if hasattr(field, 'max_digits') and hasattr(field, 'decimal_places'):
            attrs['max_digits'] = field.max_digits
            attrs['decimal_places'] = field.decimal_places
            pg_type = f"numeric({field.max_digits},{field.decimal_places})"
    
    # リレーションフィールドの処理
    elif field_type in ['ForeignKey', 'OneToOneField']:
        # 参照先のテーブル名とカラム名を取得
        related_model = field.related_model
        attrs['references'] = {
            'table': related_model._meta.db_table,
            'column': related_model._meta.pk.name
        }
        
        # 外部キー制約の名前
        constraint_name = f"{field.model._meta.db_table}_{field.name}_fkey"
        attrs['constraint_name'] = constraint_name
    
    # Nullableの設定
    if hasattr(field, 'null'):
        attrs['nullable'] = field.null
    
    # デフォルト値の設定
    if field.default is not models.fields.NOT_PROVIDED:
        # callable型のデフォルト値の場合は実行して値を取得
        default_value = field.default() if callable(field.default) else field.default
        attrs['default'] = default_value
    
    return pg_type, attrs

def get_model_table_schema(model: Type[models.Model]) -> Dict[str, Any]:
    """
    DjangoモデルからSupabaseテーブルスキーマ情報を生成します。
    
    Args:
        model: Djangoモデルクラス
        
    Returns:
        テーブルスキーマの辞書
    """
    fields_info = {}
    primary_key = None
    foreign_keys = []
    
    for field in model._meta.fields:
        field_name = field.column
        pg_type, attrs = get_django_field_type(field)
        
        # 主キーの特定
        if field.primary_key:
            primary_key = field_name
        
        # 外部キーの処理
        if isinstance(field, RelatedField) and hasattr(field, 'remote_field'):
            # ForeignKeyやOneToOneFieldの場合
            if pg_type:  # ManyToManyは別テーブルなのでスキップ
                ref_info = attrs.get('references', {})
                if ref_info:
                    foreign_keys.append({
                        'column': field_name,
                        'references': ref_info,
                        'name': attrs.get('constraint_name')
                    })
        
        fields_info[field_name] = {
            'type': pg_type,
            'nullable': attrs.get('nullable', False),
        }
        
        # デフォルト値がある場合
        if 'default' in attrs:
            fields_info[field_name]['default'] = attrs['default']
    
    return {
        'table_name': model._meta.db_table,
        'fields': fields_info,
        'primary_key': primary_key,
        'foreign_keys': foreign_keys
    }

def create_supabase_table(model: Type[models.Model]) -> bool:
    """
    Djangoモデルに基づいてSupabaseにテーブルを作成します。
    
    Args:
        model: Djangoモデルクラス
        
    Returns:
        成功した場合はTrue、それ以外はFalse
    """
    try:
        schema = get_model_table_schema(model)
        supabase = get_supabase_client()
        
        # テーブル名
        table_name = schema['table_name']
        
        # SQL文の作成
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
        
        # フィールド定義
        field_defs = []
        for field_name, field_info in schema['fields'].items():
            field_def = f"  {field_name} {field_info['type']}"
            
            if not field_info.get('nullable', False):
                field_def += " NOT NULL"
                
            if 'default' in field_info:
                default_val = field_info['default']
                if isinstance(default_val, str):
                    default_val = f"'{default_val}'"
                elif default_val is None:
                    default_val = "NULL"
                elif isinstance(default_val, bool):
                    default_val = str(default_val).lower()
                field_def += f" DEFAULT {default_val}"
                
            field_defs.append(field_def)
        
        # 主キー制約
        if schema['primary_key']:
            field_defs.append(f"  PRIMARY KEY ({schema['primary_key']})")
        
        sql += ",\n".join(field_defs)
        sql += "\n);"
        
        # テーブル作成
        try:
            supabase.rpc('execute_sql', { 'sql': sql }).execute()
        except Exception as rpc_err:
            error_context = f"テーブル {table_name} の作成に失敗しました"
            extra_info = {'table': table_name, 'sql': sql}
            log_error_details(rpc_err, error_context, extra_info)
            # より具体的な例外に変換
            raise SupabaseOperationError(f"{error_context}: {str(rpc_err)}")
        
        # 外部キー制約の作成
        for fk in schema['foreign_keys']:
            fk_sql = f"""
            ALTER TABLE {table_name} 
            ADD CONSTRAINT {fk['name']} 
            FOREIGN KEY ({fk['column']}) 
            REFERENCES {fk['references']['table']}({fk['references']['column']});
            """
            try:
                supabase.rpc('execute_sql', { 'sql': fk_sql }).execute()
            except Exception as fk_err:
                error_context = f"外部キー制約 {fk['name']} の作成に失敗しました"
                extra_info = {'table': table_name, 'constraint': fk['name'], 'sql': fk_sql}
                log_error_details(fk_err, error_context, extra_info)
                # このエラーはログに記録するが、致命的とはしない（テーブル自体は作成済み）
                logger.warning(f"{error_context}。テーブルは作成されましたが、外部キー制約の追加に失敗しました。")
        
        logger.info(f"テーブル {table_name} を作成しました")
        return True
        
    except SupabaseSyncError as sse:
        # 既に処理済みのSupabaseSyncError
        return False
    except Exception as e:
        error_context = f"テーブル作成中に予期しないエラーが発生しました"
        extra_info = {'model': model.__name__, 'table': getattr(model, '_meta', {}).get('db_table', 'unknown')}
        log_error_details(e, error_context, extra_info)
        return False

def alter_supabase_table(model: Type[models.Model]) -> bool:
    """
    既存のSupabaseテーブルをDjangoモデルに合わせて変更します。
    
    Args:
        model: Djangoモデルクラス
        
    Returns:
        成功した場合はTrue、それ以外はFalse
    """
    try:
        schema = get_model_table_schema(model)
        supabase = get_supabase_client()
        table_name = schema['table_name']
        
        # 既存のテーブル構造を取得（RPC失敗時はinformation_schema.columnsへフォールバック）
        try:
            rpc_res = supabase.rpc("select_columns", {"p_table_name": table_name}).execute()
            columns_data = rpc_res.data
        except Exception as col_err:
            log_error_details(col_err, f"テーブル {table_name} のカラム情報取得に失敗しました (RPC)、フォールバックを試みます", {'table': table_name})
            # pg_catalogを利用したフォールバック
            pg_fallback_sql = f"""
            SELECT a.attname AS column_name,
                   pg_catalog.format_type(a.atttypid, a.atttypmod) AS data_type,
                   (NOT a.attnotnull) AS is_nullable
            FROM pg_catalog.pg_attribute a
            JOIN pg_catalog.pg_class c ON a.attrelid = c.oid
            JOIN pg_catalog.pg_namespace n ON c.relnamespace = n.oid
            WHERE c.relname = '{table_name}' AND n.nspname = 'public'
              AND a.attnum > 0 AND NOT a.attisdropped;
            """
            try:
                fb_res = supabase.rpc('execute_sql', {'sql': pg_fallback_sql}).execute()
                columns_data = fb_res.data
                logger.info(f"pg_catalogフォールバックでテーブル {table_name} のカラム情報を取得しました")
            except Exception as fb_err:
                error_context = f"テーブル {table_name} のカラム情報取得フォールバックに失敗しました"
                log_error_details(fb_err, error_context, {'table': table_name, 'sql': pg_fallback_sql})
                raise SupabaseOperationError(f"{error_context}: {str(fb_err)}")
        if not columns_data:
            error_context = f"テーブル {table_name} のカラム情報が取得できませんでした"
            logger.error(error_context)
            raise SupabaseDataError(error_context)
        existing_columns = {col['column_name']: col for col in columns_data}
        model_columns = set(schema['fields'].keys())
        db_columns = set(existing_columns.keys())
        
        # 新しいカラムを追加
        for col_name in model_columns - db_columns:
            field_info = schema['fields'][col_name]
            add_col_sql = f"ALTER TABLE {table_name} ADD COLUMN {col_name} {field_info['type']}"
            
            if not field_info.get('nullable', False):
                add_col_sql += " NOT NULL"
                
            if 'default' in field_info:
                default_val = field_info['default']
                if isinstance(default_val, str):
                    default_val = f"'{default_val}'"
                elif default_val is None:
                    default_val = "NULL"
                elif isinstance(default_val, bool):
                    default_val = str(default_val).lower()
                add_col_sql += f" DEFAULT {default_val}"
            
            try:
                supabase.rpc('execute_sql', { 'sql': add_col_sql }).execute()
                logger.info(f"カラム {col_name} をテーブル {table_name} に追加しました")
            except Exception as add_err:
                error_context = f"カラム {col_name} の追加に失敗しました"
                extra_info = {'table': table_name, 'column': col_name, 'sql': add_col_sql}
                log_error_details(add_err, error_context, extra_info)
                # 続行する（他のカラムは追加できる可能性がある）
                logger.warning(f"{error_context}。処理を続行します。")
        
        # 型の変更が必要なカラムを変更
        for col_name in model_columns.intersection(db_columns):
            field_info = schema['fields'][col_name]
            db_info = existing_columns[col_name]
            
            # 型が異なる場合は変更
            if field_info['type'] != db_info['data_type']:
                alter_col_sql = f"ALTER TABLE {table_name} ALTER COLUMN {col_name} TYPE {field_info['type']} USING {col_name}::{field_info['type']}"
                try:
                    supabase.rpc('execute_sql', { 'sql': alter_col_sql }).execute()
                    logger.info(f"カラム {col_name} の型を {field_info['type']} に変更しました")
                except Exception as type_err:
                    error_context = f"カラム {col_name} の型変更に失敗しました"
                    extra_info = {
                        'table': table_name, 
                        'column': col_name, 
                        'current_type': db_info['data_type'],
                        'desired_type': field_info['type'],
                        'sql': alter_col_sql
                    }
                    log_error_details(type_err, error_context, extra_info)
                    # 続行する（他のカラムは変更できる可能性がある）
                    logger.warning(f"{error_context}。処理を続行します。")
            
            # NULL制約の変更
            is_nullable = db_info['is_nullable'].lower() == 'yes'
            should_be_nullable = field_info.get('nullable', False)
            
            if is_nullable != should_be_nullable:
                null_sql = f"ALTER TABLE {table_name} ALTER COLUMN {col_name} "
                null_sql += "DROP NOT NULL" if should_be_nullable else "SET NOT NULL"
                try:
                    supabase.rpc('execute_sql', { 'sql': null_sql }).execute()
                    logger.info(f"カラム {col_name} のNULL制約を {'解除' if should_be_nullable else '設定'} しました")
                except Exception as null_err:
                    error_context = f"カラム {col_name} のNULL制約変更に失敗しました"
                    extra_info = {'table': table_name, 'column': col_name, 'sql': null_sql}
                    log_error_details(null_err, error_context, extra_info)
                    # 続行する
                    logger.warning(f"{error_context}。処理を続行します。")
        
        # 削除対象のカラムを確認（安全のため実際には削除しない）
        columns_to_remove = db_columns - model_columns
        if columns_to_remove:
            logger.warning(f"テーブル {table_name} に不要なカラムがあります: {', '.join(columns_to_remove)}。"
                          "安全のため自動削除は行いません。手動で削除してください。")
        
        return True
        
    except SupabaseSyncError as sse:
        # 既に処理済みのSupabaseSyncError
        return False
    except Exception as e:
        error_context = f"テーブル変更中に予期しないエラーが発生しました"
        extra_info = {'model': model.__name__, 'table': getattr(model, '_meta', {}).get('db_table', 'unknown')}
        log_error_details(e, error_context, extra_info)
        return False

def sync_django_model_to_supabase(model: Type[models.Model]) -> bool:
    """
    指定したDjangoモデルをSupabaseと同期します。
    テーブルが存在しなければ作成し、存在すれば必要な変更を行います。
    
    Args:
        model: Djangoモデルクラス
        
    Returns:
        同期が成功したらTrue、失敗したらFalse
    """
    try:
        if not hasattr(model, 'supabase_table') or not model.supabase_table:
            logger.warning(f"モデル {model.__name__} はsupabase_tableが設定されていないため同期できません")
            return False
        
        try:
            supabase = get_supabase_client()
        except Exception as conn_err:
            error_context = f"Supabaseクライアント取得中にエラーが発生しました"
            log_error_details(conn_err, error_context)
            raise SupabaseConnectionError(f"{error_context}: {str(conn_err)}")
            
        table_name = model._meta.db_table
        
        # テーブルの存在確認 - 複数の方法でフォールバックする拡張アプローチ
        try:
            table_exists = check_table_exists_with_fallback(supabase, table_name)
        except Exception as check_err:
            error_context = f"テーブル {table_name} の存在確認中にエラーが発生しました"
            extra_info = {'table': table_name}
            log_error_details(check_err, error_context, extra_info)
            raise SupabaseOperationError(f"{error_context}: {str(check_err)}")
        
        # 同期処理の実行
        if not table_exists:
            logger.info(f"テーブル {table_name} が存在しないため作成します")
            # テーブルが存在しない場合は作成
            return create_supabase_table(model)
        else:
            logger.info(f"テーブル {table_name} が存在するため変更します")
            # テーブルが存在する場合は変更
            return alter_supabase_table(model)
            
    except SupabaseSyncError as sse:
        # 既に処理済みのSupabaseSyncError
        logger.error(f"モデル {model.__name__} の同期中にエラーが発生しました: {str(sse)}")
        return False
    except Exception as e:
        error_context = f"モデル同期中に予期しないエラーが発生しました"
        extra_info = {'model': model.__name__}
        log_error_details(e, error_context, extra_info)
        return False

def check_table_exists_with_fallback(supabase, table_name: str) -> bool:
    """
    テーブルが存在するかどうかを複数の方法でチェックします。
    一つの方法が失敗した場合、別の方法にフォールバックします。
    """
    # エラーメッセージ収集用
    error_messages = []

    # 方法1: REST API経由のSELECTで存在確認
    try:
        supabase.table(table_name).select("*").limit(1).execute()
        logger.debug(f"REST APIでテーブル {table_name} の存在を確認: 成功")
        return True
    except Exception as e:
        msg = str(e)
        if "does not exist" in msg or "relation" in msg:
            logger.debug(f"REST APIでテーブル {table_name} の存在を確認: 存在しません")
            return False
        warning_msg = f"REST APIによるテーブル確認に失敗しました: {msg}"
        logger.warning(warning_msg)
        error_messages.append(warning_msg)

    # 方法2: pg_catalog.pg_tablesを使った確認
    try:
        pg_sql = f"""
        SELECT EXISTS (
            SELECT 1 FROM pg_catalog.pg_tables
            WHERE schemaname='public' AND tablename='{table_name}'
        ) AS table_exists;
        """
        result = supabase.rpc('execute_sql', {'sql': pg_sql}).execute()
        exists = bool(result.data and result.data[0].get('table_exists'))
        logger.debug(f"pg_catalog方式でテーブル {table_name} の存在を確認: {exists}")
        return exists
    except Exception as e:
        warning_msg = f"pg_catalog方式によるテーブル確認に失敗しました: {str(e)}"
        logger.warning(warning_msg)
        error_messages.append(warning_msg)

    # 方法3: RPCメソッドを最後の手段として使用
    try:
        result = supabase.rpc("check_table_exists", {"p_table_name": table_name}).execute()
        if result.data and len(result.data) > 0:
            exists = result.data[0].get('table_exists', False)
            logger.debug(f"RPCでテーブル {table_name} の存在を確認: {exists}")
            return exists
    except Exception as e:
        warning_msg = f"RPCメソッドによるテーブル確認に失敗しました: {str(e)}"
        logger.warning(warning_msg)
        error_messages.append(warning_msg)

    # 全ての方法が失敗した場合
    error_summary = "\n".join(error_messages)
    logger.error(f"テーブル {table_name} の存在確認に全ての方法が失敗しました。\n{error_summary}")
    suppress = getattr(settings, 'SUPABASE_SUPPRESS_TABLE_CHECK_ERRORS', False)
    if suppress:
        logger.warning("テーブル確認エラーを抑制し、存在しないと判断します。")
        return False
    raise SupabaseOperationError(f"テーブル {table_name} の存在確認に失敗しました")

def sync_all_models_to_supabase() -> Dict[str, bool]:
    """
    SupabaseModelMixinを継承した全てのモデルをSupabaseと同期します。
    
    Returns:
        各モデルの同期結果を含む辞書 {モデル名: 成功/失敗}
    """
    results = {}
    models = get_supabase_models()
    
    for model in models:
        model_name = model.__name__
        results[model_name] = sync_django_model_to_supabase(model)
        
    return results

def get_data_migration_sql(model: Type[models.Model], instances: List[models.Model]) -> str:
    """
    モデルインスタンスのリストからSUPABASEへのデータ移行用SQLを生成します。
    
    Args:
        model: Djangoモデルクラス
        instances: モデルインスタンスのリスト
        
    Returns:
        データ挿入用のSQL文
    """
    if not instances:
        return ""
    
    table_name = model._meta.db_table
    
    # インスタンスからデータを抽出
    rows = []
    field_names = []
    
    # フィールド名の抽出（最初のインスタンスから）
    for field in model._meta.fields:
        if not field.primary_key or not field.auto_created:  # 自動生成される主キーはスキップ
            field_names.append(field.column)
    
    # インスタンスごとのデータ抽出
    for instance in instances:
        row_data = []
        for field_name in field_names:
            field = model._meta.get_field(field_name)
            value = getattr(instance, field_name)
            
            # NULL処理
            if value is None:
                row_data.append("NULL")
                continue
                
            # 型に応じた形式化
            if isinstance(value, str):
                # エスケープ処理
                escaped = value.replace("'", "''")
                row_data.append(f"'{escaped}'")
            elif isinstance(value, bool):
                row_data.append(str(value).lower())
            elif isinstance(value, (int, float)):
                row_data.append(str(value))
            elif hasattr(value, 'isoformat'):  # 日付・時間型
                row_data.append(f"'{value.isoformat()}'")
            elif isinstance(value, dict) or isinstance(value, list):
                # JSON型
                json_str = json.dumps(value).replace("'", "''")
                row_data.append(f"'{json_str}'")
            else:
                # その他の型
                row_data.append(f"'{str(value)}'")
        
        rows.append("(" + ", ".join(row_data) + ")")
    
    # INSERT文の生成
    fields_str = ", ".join(field_names)
    values_str = ",\n  ".join(rows)
    
    sql = f"""
INSERT INTO {table_name} ({fields_str})
VALUES
  {values_str}
ON CONFLICT DO NOTHING;
"""
    
    return sql

def get_model_cleanup_sql(model: Type[models.Model]) -> str:
    """
    同期前にSupabaseテーブルをクリーンアップするためのSQL文を生成します。
    
    Args:
        model: Djangoモデルクラス
        
    Returns:
        テーブルクリーンアップ用のSQL文
    """
    table_name = model._meta.db_table
    return f"DELETE FROM {table_name};"

def post_migration_sync_handler(sender, **kwargs):
    """
    Djangoマイグレーション後に自動的に呼び出される関数。
    全てのSupabaseモデルをSupabaseに同期します。
    
    Args:
        sender: シグナルを送信したアプリケーション
        **kwargs: シグナルから渡される追加パラメータ
    
    Djangoのpost_migrateシグナルハンドラとして使用します。
    """
    import sys
    import time
    from django.core.management import color
    
    # 処理時間計測開始
    start_time = time.time()
    
    # カラー出力のためのスタイルを取得
    style = color.color_style()
    
    print(f"=== Supabase同期ハンドラ開始 ===", file=sys.stderr)
    print(f"シグナル受信: sender={sender}, apps={kwargs.get('apps')}", file=sys.stderr)
    
    # アプリケーション名を取得（ロギング用）
    app_name = sender.name if hasattr(sender, 'name') else 'unknown'
    print(f"アプリケーション名: {app_name}", file=sys.stderr)
    
    # 設定でAutoSyncが有効になっているか確認
    auto_sync = getattr(settings, 'SUPABASE_AUTO_SYNC', False)
    print(f"SUPABASE_AUTO_SYNC: {auto_sync}", file=sys.stderr)
    
    if not auto_sync:
        logger.info(f"マイグレーション後の自動Supabase同期が無効です（app: {app_name}）")
        print(f"{style.WARNING('注意:')} マイグレーション後の自動Supabase同期が無効です（app: {app_name}）", file=sys.stderr)
        print(f"自動同期を有効にするには .env.development ファイルで SUPABASE_AUTO_SYNC=True を設定してください。", file=sys.stderr)
        print(f"または手動で同期を実行: python manage.py sync_supabase", file=sys.stderr)
        return
    
    # Supabaseの接続情報が設定されているか確認
    has_connection_info = all([settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY])
    print(f"Supabase接続情報: URL={bool(settings.SUPABASE_URL)}, SERVICE_KEY={bool(settings.SUPABASE_SERVICE_KEY)}", file=sys.stderr)
    
    if not has_connection_info:
        logger.warning(f"Supabase接続情報が設定されていないため、同期をスキップします（app: {app_name}）")
        print(f"{style.ERROR('エラー:')} Supabase接続情報が設定されていないため、同期をスキップします（app: {app_name}）", file=sys.stderr)
        print(f"接続情報を設定するには .env.development ファイルを確認してください。", file=sys.stderr)
        return
    
    try:
        logger.info(f"アプリケーション '{app_name}' のマイグレーション後Supabase同期を開始します")
        print(f"{style.SUCCESS('開始:')} アプリケーション '{app_name}' のマイグレーション後Supabase同期を開始します", file=sys.stderr)
        
        # このアプリケーションのSupabaseモデルのみを取得
        app_models = []
        all_models = get_supabase_models()
        print(f"取得したSupabaseモデル数: {len(all_models)}", file=sys.stderr)
        
        for model in all_models:
            model_app = model._meta.app_label
            print(f"モデル確認: {model.__name__}, app_label={model_app}", file=sys.stderr)
            if model_app == app_name or app_name == 'techskillsquiz':  # 'techskillsquiz'はメインアプリなので全てのモデルを対象
                app_models.append(model)
        
        print(f"同期対象モデル数: {len(app_models)}", file=sys.stderr)
        
        if not app_models:
            logger.info(f"アプリケーション '{app_name}' にはSupabaseと同期するモデルがありません")
            print(f"{style.WARNING('注意:')} アプリケーション '{app_name}' にはSupabaseと同期するモデルがありません", file=sys.stderr)
            print(f"モデルにSupabaseModelMixinを継承させ、supabase_table属性を設定してください。", file=sys.stderr)
            return
        
        # モデルごとに同期
        results = {}
        total_count = len(app_models)
        current = 0
        
        for model in app_models:
            current += 1
            model_name = f"{model._meta.app_label}.{model.__name__}"
            logger.info(f"モデル '{model_name}' の同期を開始します")
            print(f"[{current}/{total_count}] モデル '{model_name}' の同期を開始します...", file=sys.stderr)
            
            try:
                start_model_time = time.time()
                success = sync_django_model_to_supabase(model)
                model_time = time.time() - start_model_time
                results[model_name] = success
                
                if success:
                    logger.info(f"モデル '{model_name}' の同期が成功しました ({model_time:.2f}秒)")
                    print(f"{style.SUCCESS('✓')} モデル '{model_name}' の同期が成功しました ({model_time:.2f}秒)", file=sys.stderr)
                else:
                    logger.error(f"モデル '{model_name}' の同期に失敗しました ({model_time:.2f}秒)")
                    print(f"{style.ERROR('✗')} モデル '{model_name}' の同期に失敗しました ({model_time:.2f}秒)", file=sys.stderr)
            except Exception as e:
                logger.exception(f"モデル '{model_name}' の同期中に例外が発生しました: {str(e)}")
                print(f"{style.ERROR('✗')} モデル '{model_name}' の同期中に例外が発生しました: {str(e)}", file=sys.stderr)
                import traceback
                traceback.print_exc(file=sys.stderr)
                results[model_name] = False
        
        # 処理時間を計算
        total_time = time.time() - start_time
        
        # 結果の集計
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)
        
        if total_count > 0:
            logger.info(f"アプリケーション '{app_name}' のSupabase同期が完了しました。{success_count}/{total_count}のモデルが正常に同期されました。(合計: {total_time:.2f}秒)")
            print(f"{style.SUCCESS('完了:')} アプリケーション '{app_name}' のSupabase同期が完了しました。", file=sys.stderr)
            print(f"{style.SUCCESS(f'{success_count}/{total_count}')}のモデルが正常に同期されました。(合計: {total_time:.2f}秒)", file=sys.stderr)
            
            # 失敗したモデルがあれば警告
            failed_models = [model for model, success in results.items() if not success]
            if failed_models:
                logger.warning(f"次のモデルの同期に失敗しました: {', '.join(failed_models)}")
                print(f"{style.WARNING('警告:')} 次のモデルの同期に失敗しました:", file=sys.stderr)
                for model in failed_models:
                    print(f"  - {style.ERROR(model)}", file=sys.stderr)
                print(f"手動で同期を再試行: python manage.py sync_supabase --model=[モデル名]", file=sys.stderr)
        
    except Exception as e:
        logger.exception(f"マイグレーション後のSupabase同期中に予期しない例外が発生しました: {str(e)}")
        print(f"{style.ERROR('致命的エラー:')} マイグレーション後のSupabase同期中に予期しない例外が発生しました: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
    
    finally:
        print(f"=== Supabase同期ハンドラ終了 ===", file=sys.stderr) 