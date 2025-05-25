import { useState, useEffect } from 'react';
import { ActivityHistory } from '../lib/api/types';
import { QuizService } from '../lib/api/services/quiz.service';
import { getAccessToken } from '../lib/api/token';
import { useAuth } from '../lib/contexts/AuthContext';

export interface UseRecentActivitiesReturn {
  activities: ActivityHistory[];
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

export function useRecentActivities(limit: number = 5): UseRecentActivitiesReturn {
  const [activities, setActivities] = useState<ActivityHistory[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated, onAuthChange } = useAuth();

  const quizService = new QuizService();

  const fetchActivities = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // 認証状態を事前にチェック
      const token = getAccessToken();
      
      if (!token || !isAuthenticated) {
        setError('活動履歴を表示するにはログインしてください');
        setActivities([]);
        setLoading(false);
        return;
      }
      
      const data = await quizService.getRecentActivities(limit);
      setActivities(data || []); // データがnullやundefinedの場合は空配列を設定
    } catch (err: any) {
      console.error('最近の活動履歴の取得に失敗しました:', err);
      
      // 認証エラーや実際のサーバーエラーの場合のみエラーとして扱う
      // 404やデータなしの場合は正常な空状態として扱う
      if (err?.response?.status === 401) {
        setError('活動履歴を表示するにはログインしてください');
      } else if (err?.response?.status >= 500) {
        setError('サーバーエラーが発生しました');
      } else if (err?.code === 'ERR_NETWORK') {
        setError('ネットワークエラーが発生しました');
      } else {
        // その他の場合（404など）は単純に空配列を設定し、エラーとしては扱わない
        console.log('活動履歴が見つかりませんでした（正常な状態）');
      }
      
      setActivities([]);
    } finally {
      setLoading(false);
    }
  };

  // 初回ロード
  useEffect(() => {
    fetchActivities();
  }, [limit]);

  // 認証状態の変化を監視
  useEffect(() => {
    const unsubscribe = onAuthChange((authenticated) => {
      if (!authenticated) {
        // ログアウト時は即座にエラーメッセージを表示
        setError('活動履歴を表示するにはログインしてください');
        setActivities([]);
        setLoading(false);
      } else {
        // ログイン時は活動履歴を再取得
        fetchActivities();
      }
    });

    return unsubscribe;
  }, [onAuthChange]);

  return {
    activities,
    loading,
    error,
    refetch: fetchActivities
  };
} 