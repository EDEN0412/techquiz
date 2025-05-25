import { useState, useEffect } from 'react';
import { UserStatsSummary } from '../lib/api/types';
import { QuizService } from '../lib/api/services/quiz.service';
import { useAuth } from '../lib/contexts/AuthContext';

export interface UseUserStatsReturn {
  stats: UserStatsSummary | null;
  loading: boolean;
  error: string | null;
  refetch: () => void;
}

export function useUserStats(): UseUserStatsReturn {
  const [stats, setStats] = useState<UserStatsSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { isAuthenticated, onAuthChange } = useAuth();

  const quizService = new QuizService();

  const fetchStats = async () => {
    try {
      setLoading(true);
      setError(null);
      
      if (!isAuthenticated) {
        setStats(null);
        setLoading(false);
        return;
      }
      
      const data = await quizService.getUserStatsSummary();
      setStats(data);
    } catch (err) {
      console.error('統計情報の取得に失敗しました:', err);
      setError('統計情報を取得できませんでした');
    } finally {
      setLoading(false);
    }
  };

  // 初回ロード
  useEffect(() => {
    fetchStats();
  }, []);

  // 認証状態の変化を監視
  useEffect(() => {
    const unsubscribe = onAuthChange((authenticated) => {
      if (!authenticated) {
        // ログアウト時は即座に統計情報をリセット
        setStats(null);
        setError(null);
        setLoading(false);
      } else {
        // ログイン時は統計情報を再取得
        fetchStats();
      }
    });

    return unsubscribe;
  }, [onAuthChange]);

  return {
    stats,
    loading,
    error,
    refetch: fetchStats
  };
} 