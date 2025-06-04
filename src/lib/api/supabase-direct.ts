/**
 * Supabase直接接続クライアント（開発・テスト用）
 */
import { Difficulty, Category } from './types';

// Supabaseローカル環境の設定
const SUPABASE_URL = 'http://127.0.0.1:54321';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0';

/**
 * Supabase REST APIから難易度データを取得
 */
export async function fetchDifficultyLevelsFromSupabase(): Promise<Difficulty[]> {
  try {
    const response = await fetch(`${SUPABASE_URL}/rest/v1/difficulty_level?select=*&order=level.asc`, {
      headers: {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    // Supabaseのデータ形式をフロントエンドの型に変換
    return data.map((item: any): Difficulty => ({
      id: item.id,
      name: item.name,
      slug: item.slug,
      level: item.level,
      description: item.description || '',
      point_multiplier: item.point_multiplier,
      time_limit: item.time_limit,
      created_at: item.created_at,
      updated_at: item.updated_at,
    }));
  } catch (error) {
    console.error('Supabaseからの難易度データ取得に失敗しました:', error);
    throw error;
  }
}

/**
 * Supabase REST APIからカテゴリデータを取得
 */
export async function fetchCategoriesFromSupabase(): Promise<Category[]> {
  try {
    const response = await fetch(`${SUPABASE_URL}/rest/v1/category?select=*&order=display_order.asc`, {
      headers: {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    // Supabaseのデータ形式をフロントエンドの型に変換
    return data.map((item: any): Category => ({
      id: item.id,
      name: item.name,
      slug: item.slug,
      description: item.description || '',
      is_active: item.is_active,
      display_order: item.display_order,
      created_at: item.created_at,
      updated_at: item.updated_at,
    }));
  } catch (error) {
    console.error('Supabaseからのカテゴリデータ取得に失敗しました:', error);
    throw error;
  }
}
