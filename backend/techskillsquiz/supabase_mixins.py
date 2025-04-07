"""
Supabase integration mixins for Django models.

このモジュールはDjangoモデルからSupabaseテーブルにアクセスするためのミックスインを提供します。
"""

from typing import Dict, List, Any, Optional, Union

from .supabase import get_supabase_client


class SupabaseModelMixin:
    """
    DjangoモデルにSupabaseテーブルへのアクセス機能を追加するミックスイン。
    """
    
    # Supabaseのテーブル名（サブクラスでオーバーライドする）
    supabase_table: str = None
    
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