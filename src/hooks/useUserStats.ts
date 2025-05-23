import { useState, useEffect } from 'react';
import { UserStatsSummary } from '../lib/api/types';
import { QuizService } from '../lib/api/services/quiz.service';

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

  const quizService = new QuizService();

  const fetchStats = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await quizService.getUserStatsSummary();
      setStats(data);
    } catch (err) {
      console.error('統計情報の取得に失敗しました:', err);
      setError('統計情報を取得できませんでした');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  return {
    stats,
    loading,
    error,
    refetch: fetchStats
  };
} 