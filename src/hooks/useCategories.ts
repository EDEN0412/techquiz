import { useState, useEffect, useCallback } from 'react';
import { Category } from '../lib/api/types';

// モックデータ（一時的に使用）
const mockCategories: Category[] = [
  {
    id: 1,
    name: 'HTML & CSS',
    slug: 'html-css',
    description: 'Webの基礎とスタイリングを習得',
    is_active: true,
    display_order: 1,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 2,
    name: 'Ruby',
    slug: 'ruby',
    description: 'オブジェクト指向スクリプト言語の基礎',
    is_active: true,
    display_order: 2,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 3,
    name: 'Ruby on Rails',
    slug: 'ruby-rails',
    description: 'Rubyベースの高速Webアプリケーション開発',
    is_active: true,
    display_order: 3,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 4,
    name: 'JavaScript',
    slug: 'javascript',
    description: 'Web開発に不可欠なプログラミング言語',
    is_active: true,
    display_order: 4,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 5,
    name: 'Webアプリケーション基礎',
    slug: 'web-app-basic',
    description: 'Webアプリ開発の基礎知識とアーキテクチャ',
    is_active: true,
    display_order: 5,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 6,
    name: 'Python',
    slug: 'python',
    description: '汎用性の高い読みやすいプログラミング言語',
    is_active: true,
    display_order: 6,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 7,
    name: 'Git',
    slug: 'git',
    description: 'バージョン管理とチーム開発',
    is_active: true,
    display_order: 7,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 8,
    name: 'Linux コマンド',
    slug: 'linux',
    description: '基本的なターミナル操作',
    is_active: true,
    display_order: 8,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 9,
    name: 'データベース',
    slug: 'database',
    description: 'SQLとデータベース管理',
    is_active: true,
    display_order: 9,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  },
];

// 設定フラグ - Supabaseから実際のデータを取得するように変更
const USE_MOCK_DATA = false;

export function useCategories() {
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchCategories = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      if (USE_MOCK_DATA) {
        // モックデータを使用（開発用）
        await new Promise(resolve => setTimeout(resolve, 500)); // ローディング状態をシミュレート
        const sortedCategories = mockCategories
          .filter(category => category.is_active)
          .sort((a, b) => a.display_order - b.display_order);
        setCategories(sortedCategories);
      } else {
        // Supabaseから直接データを取得
        const { fetchCategoriesFromSupabase } = await import('../lib/api/supabase-direct');
        const categoriesData = await fetchCategoriesFromSupabase();
        
        const sortedCategories = categoriesData
          .filter(category => category.is_active)
          .sort((a, b) => a.display_order - b.display_order);
          
        setCategories(sortedCategories);
      }
      
    } catch (err) {
      console.error('カテゴリーの取得に失敗しました:', err);
      
      // API失敗時はモックデータにフォールバック
      if (!USE_MOCK_DATA) {
        console.log('Supabase APIが失敗したため、モックデータを使用します');
        const sortedCategories = mockCategories
          .filter(category => category.is_active)
          .sort((a, b) => a.display_order - b.display_order);
        setCategories(sortedCategories);
      } else {
        setError('カテゴリーの取得に失敗しました。再試行してください。');
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchCategories();
  }, [fetchCategories]);

  const retry = () => {
    fetchCategories();
  };

  return { categories, loading, error, retry };
}
