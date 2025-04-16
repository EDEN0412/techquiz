-- information_schemaへのアクセスを行うRPC関数

-- テーブルの存在確認を行う関数
CREATE OR REPLACE FUNCTION check_table_exists(p_table_name TEXT)
RETURNS TABLE (table_exists BOOLEAN) AS $$
BEGIN
    RETURN QUERY
    SELECT EXISTS (
        SELECT 1 FROM information_schema.tables 
        WHERE table_name = p_table_name 
        AND table_schema = 'public'
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- テーブルのカラム情報を取得する関数
CREATE OR REPLACE FUNCTION select_columns(p_table_name TEXT)
RETURNS TABLE (
    column_name TEXT,
    data_type TEXT,
    is_nullable TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        columns.column_name::TEXT,
        columns.data_type::TEXT,
        columns.is_nullable::TEXT
    FROM 
        information_schema.columns
    WHERE 
        columns.table_name = p_table_name
        AND columns.table_schema = 'public';
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- 関数へのRLSポリシーが不要となるように管理者権限で実行
GRANT EXECUTE ON FUNCTION check_table_exists TO authenticated;
GRANT EXECUTE ON FUNCTION check_table_exists TO anon;
GRANT EXECUTE ON FUNCTION check_table_exists TO service_role;

GRANT EXECUTE ON FUNCTION select_columns TO authenticated;
GRANT EXECUTE ON FUNCTION select_columns TO anon;
GRANT EXECUTE ON FUNCTION select_columns TO service_role;
