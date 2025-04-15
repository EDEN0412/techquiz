"""
Supabase Sync Utilities

このモジュールはDjangoモデルとSupabaseテーブルの同期に関するユーティリティ関数を提供します。
マイグレーション後にDjangoモデルの変更をSupabaseテーブルに反映するための機能を含みます。
"""

import logging
from typing import Type, Dict, Any, List, Optional, Tuple, Set
import inspect
import json
from django.db import models
from django.apps import apps
from django.db.models.fields import Field
from django.db.models.fields.related import RelatedField
from django.conf import settings

from .supabase import get_supabase_client
from .supabase_mixins import SupabaseModelMixin

logger = logging.getLogger(__name__)

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
                print(f"    継承チェックエラー: {model.__name__}, {e}", file=sys.stderr)
                
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
        supabase.table(table_name).query(sql)
        
        # 外部キー制約の作成
        for fk in schema['foreign_keys']:
            fk_sql = f"""
            ALTER TABLE {table_name} 
            ADD CONSTRAINT {fk['name']} 
            FOREIGN KEY ({fk['column']}) 
            REFERENCES {fk['references']['table']}({fk['references']['column']});
            """
            supabase.table(table_name).query(fk_sql)
        
        logger.info(f"テーブル {table_name} を作成しました")
        return True
        
    except Exception as e:
        logger.error(f"テーブル作成中にエラーが発生しました: {str(e)}")
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
        
        # 既存のテーブル構造を取得
        result = supabase.table("information_schema.columns").select(
            "column_name", "data_type", "is_nullable"
        ).eq("table_name", table_name).execute()
        
        existing_columns = {col['column_name']: col for col in result.data}
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
            
            supabase.table(table_name).query(add_col_sql)
            logger.info(f"カラム {col_name} をテーブル {table_name} に追加しました")
        
        # 型の変更が必要なカラムを変更
        for col_name in model_columns.intersection(db_columns):
            field_info = schema['fields'][col_name]
            db_info = existing_columns[col_name]
            
            # 型が異なる場合は変更
            if field_info['type'] != db_info['data_type']:
                alter_col_sql = f"ALTER TABLE {table_name} ALTER COLUMN {col_name} TYPE {field_info['type']} USING {col_name}::{field_info['type']}"
                supabase.table(table_name).query(alter_col_sql)
                logger.info(f"カラム {col_name} の型を {field_info['type']} に変更しました")
            
            # NULL制約の変更
            is_nullable = db_info['is_nullable'].lower() == 'yes'
            should_be_nullable = field_info.get('nullable', False)
            
            if is_nullable != should_be_nullable:
                null_sql = f"ALTER TABLE {table_name} ALTER COLUMN {col_name} "
                null_sql += "DROP NOT NULL" if should_be_nullable else "SET NOT NULL"
                supabase.table(table_name).query(null_sql)
                logger.info(f"カラム {col_name} のNULL制約を {'解除' if should_be_nullable else '設定'} しました")
        
        # 削除対象のカラムを確認（安全のため実際には削除しない）
        columns_to_remove = db_columns - model_columns
        if columns_to_remove:
            logger.warning(f"テーブル {table_name} に不要なカラムがあります: {', '.join(columns_to_remove)}。"
                          "安全のため自動削除は行いません。手動で削除してください。")
        
        return True
        
    except Exception as e:
        logger.error(f"テーブル変更中にエラーが発生しました: {str(e)}")
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
        
        supabase = get_supabase_client()
        table_name = model._meta.db_table
        
        # テーブルの存在確認
        result = supabase.table("information_schema.tables").select(
            "table_name"
        ).eq("table_name", table_name).execute()
        
        if not result.data:
            # テーブルが存在しない場合は作成
            return create_supabase_table(model)
        else:
            # テーブルが存在する場合は変更
            return alter_supabase_table(model)
            
    except Exception as e:
        logger.error(f"モデル {model.__name__} の同期中にエラーが発生しました: {str(e)}")
        return False

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
    print(f"post_migration_sync_handler: シグナル受信 sender={sender}, kwargs={kwargs}", file=sys.stderr)
    
    # アプリケーション名を取得（ロギング用）
    app_name = sender.name if hasattr(sender, 'name') else 'unknown'
    print(f"アプリケーション名: {app_name}", file=sys.stderr)
    
    # 設定でAutoSyncが有効になっているか確認
    auto_sync = getattr(settings, 'SUPABASE_AUTO_SYNC', False)
    print(f"SUPABASE_AUTO_SYNC: {auto_sync}", file=sys.stderr)
    
    if not auto_sync:
        logger.info(f"マイグレーション後の自動Supabase同期が無効です（app: {app_name}）")
        print(f"マイグレーション後の自動Supabase同期が無効です（app: {app_name}）", file=sys.stderr)
        return
    
    # Supabaseの接続情報が設定されているか確認
    has_connection_info = all([settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY])
    print(f"Supabase接続情報: URL={bool(settings.SUPABASE_URL)}, SERVICE_KEY={bool(settings.SUPABASE_SERVICE_KEY)}", file=sys.stderr)
    
    if not has_connection_info:
        logger.warning(f"Supabase接続情報が設定されていないため、同期をスキップします（app: {app_name}）")
        print(f"Supabase接続情報が設定されていないため、同期をスキップします（app: {app_name}）", file=sys.stderr)
        return
    
    try:
        logger.info(f"アプリケーション '{app_name}' のマイグレーション後Supabase同期を開始します")
        print(f"アプリケーション '{app_name}' のマイグレーション後Supabase同期を開始します", file=sys.stderr)
        
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
            print(f"アプリケーション '{app_name}' にはSupabaseと同期するモデルがありません", file=sys.stderr)
            return
        
        # モデルごとに同期
        results = {}
        for model in app_models:
            model_name = f"{model._meta.app_label}.{model.__name__}"
            logger.info(f"モデル '{model_name}' の同期を開始します")
            print(f"モデル '{model_name}' の同期を開始します", file=sys.stderr)
            
            try:
                success = sync_django_model_to_supabase(model)
                results[model_name] = success
                
                if success:
                    logger.info(f"モデル '{model_name}' の同期が成功しました")
                    print(f"モデル '{model_name}' の同期が成功しました", file=sys.stderr)
                else:
                    logger.error(f"モデル '{model_name}' の同期に失敗しました")
                    print(f"モデル '{model_name}' の同期に失敗しました", file=sys.stderr)
            except Exception as e:
                logger.exception(f"モデル '{model_name}' の同期中に例外が発生しました: {str(e)}")
                print(f"モデル '{model_name}' の同期中に例外が発生しました: {str(e)}", file=sys.stderr)
                import traceback
                traceback.print_exc()
                results[model_name] = False
        
        # 結果の集計
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)
        
        if total_count > 0:
            logger.info(f"アプリケーション '{app_name}' のSupabase同期が完了しました。{success_count}/{total_count}のモデルが正常に同期されました。")
            print(f"アプリケーション '{app_name}' のSupabase同期が完了しました。{success_count}/{total_count}のモデルが正常に同期されました。", file=sys.stderr)
            
            # 失敗したモデルがあれば警告
            failed_models = [model for model, success in results.items() if not success]
            if failed_models:
                logger.warning(f"次のモデルの同期に失敗しました: {', '.join(failed_models)}")
                print(f"次のモデルの同期に失敗しました: {', '.join(failed_models)}", file=sys.stderr)
        
    except Exception as e:
        logger.exception(f"マイグレーション後のSupabase同期中に予期しない例外が発生しました: {str(e)}")
        print(f"マイグレーション後のSupabase同期中に予期しない例外が発生しました: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc() 