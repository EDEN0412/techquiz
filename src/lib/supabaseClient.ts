import { createClient } from '@supabase/supabase-js'

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseKey = import.meta.env.VITE_SUPABASE_ANON_KEY

export const supabase = createClient(supabaseUrl, supabaseKey)

// Supabase接続テスト用関数
export async function testSupabaseConnection() {
  try {
    // サーバー時間を取得してテスト
    const { data, error } = await supabase.from('_test_connection')
      .select('*')
      .limit(1)
      .maybeSingle()
    
    if (error && error.code !== 'PGRST116') {
      // PGRST116はテーブルが存在しないエラー。接続自体は成功している
      console.error('Supabase接続エラー:', error)
      return { success: false, error }
    }
    
    // テーブルが存在しなくても接続できていれば成功と判断
    console.log('Supabase接続成功')
    return { 
      success: true, 
      message: 'Supabaseに正常に接続されました。',
      connectionDetails: {
        url: supabaseUrl,
        authenticated: !!supabase.auth.getSession()
      }
    }
  } catch (err) {
    console.error('テスト実行中にエラーが発生しました:', err)
    return { success: false, error: err }
  }
}
