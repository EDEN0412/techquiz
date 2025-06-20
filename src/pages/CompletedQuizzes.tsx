import { useState, useEffect, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/Card';
import { useAuth } from '../lib/contexts/AuthContext';
import { userService } from '../lib/api';
import { QuizResultResponse } from '../lib/api/types';

export function CompletedQuizzes() {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();
  const [completedQuizzes, setCompletedQuizzes] = useState<QuizResultResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [sortBy, setSortBy] = useState<'date' | 'score' | 'category'>('date');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');

  // 絞り込み用のstate
  const [filterCategory, setFilterCategory] = useState<string>('all');
  const [filterDifficulty, setFilterDifficulty] = useState<string>('all');
  const [filterPeriod, setFilterPeriod] = useState<string>('all');
  const [filterScoreMin, setFilterScoreMin] = useState<number>(0);
  const [filterScoreMax, setFilterScoreMax] = useState<number>(100);

  // 完了したクイズを取得する関数
  const fetchCompletedQuizzes = async () => {
    if (!isAuthenticated) {
      setError('ログインが必要です');
      setLoading(false);
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      // ユーザーのクイズ結果を取得
      const results = await userService.getUserQuizResults();
      setCompletedQuizzes(results);
    } catch (err) {
      console.error('完了クイズ取得エラー:', err);
      setError('完了したクイズの取得に失敗しました');
    } finally {
      setLoading(false);
    }
  };

  // 絞り込みとソートを適用した結果を計算
  const filteredAndSortedQuizzes = useMemo(() => {
    let filtered = completedQuizzes.filter((quiz) => {
      // カテゴリー絞り込み
      if (filterCategory !== 'all' && quiz.category_name !== filterCategory) {
        return false;
      }

      // 難易度絞り込み
      if (filterDifficulty !== 'all' && quiz.difficulty_name !== filterDifficulty) {
        return false;
      }

      // スコア範囲絞り込み
      if (quiz.percentage < filterScoreMin || quiz.percentage > filterScoreMax) {
        return false;
      }

      // 期間絞り込み
      if (filterPeriod !== 'all') {
        const completedDate = new Date(quiz.completed_at);
        const now = new Date();
        const diffDays = (now.getTime() - completedDate.getTime()) / (1000 * 60 * 60 * 24);

        switch (filterPeriod) {
          case 'week':
            if (diffDays > 7) return false;
            break;
          case 'month':
            if (diffDays > 30) return false;
            break;
          case 'quarter':
            if (diffDays > 90) return false;
            break;
        }
      }

      return true;
    });

    // ソート処理
    filtered.sort((a, b) => {
      let aValue, bValue;
      
      switch (sortBy) {
        case 'date':
          aValue = new Date(a.completed_at).getTime();
          bValue = new Date(b.completed_at).getTime();
          break;
        case 'score':
          aValue = a.percentage;
          bValue = b.percentage;
          break;
        case 'category':
          aValue = a.category_name || '';
          bValue = b.category_name || '';
          break;
        default:
          aValue = new Date(a.completed_at).getTime();
          bValue = new Date(b.completed_at).getTime();
      }
      
      if (sortOrder === 'asc') {
        return aValue < bValue ? -1 : aValue > bValue ? 1 : 0;
      } else {
        return aValue > bValue ? -1 : aValue < bValue ? 1 : 0;
      }
    });

    return filtered;
  }, [completedQuizzes, filterCategory, filterDifficulty, filterPeriod, filterScoreMin, filterScoreMax, sortBy, sortOrder]);

  // 利用可能なカテゴリーと難易度を取得
  const availableCategories = useMemo(() => {
    const categories = [...new Set(completedQuizzes.map(quiz => quiz.category_name))].filter(Boolean);
    return categories.sort();
  }, [completedQuizzes]);

  const availableDifficulties = useMemo(() => {
    const difficulties = [...new Set(completedQuizzes.map(quiz => quiz.difficulty_name))].filter(Boolean);
    return difficulties.sort();
  }, [completedQuizzes]);

  // フィルターをリセットする関数
  const resetFilters = () => {
    setFilterCategory('all');
    setFilterDifficulty('all');
    setFilterPeriod('all');
    setFilterScoreMin(0);
    setFilterScoreMax(100);
  };

  useEffect(() => {
    fetchCompletedQuizzes();
  }, [isAuthenticated]);

  // 復習機能
  const handleReviewQuiz = (quizResult: QuizResultResponse) => {
    navigate(`/quiz/review/${quizResult.quiz}`, {
      state: { fromCompletedList: true }
    });
  };

  // 詳細表示機能
  const handleViewDetails = (quizResult: QuizResultResponse) => {
    navigate(`/quiz-result/${quizResult.id}`, {
      state: { quizResult }
    });
  };

  // スコアに基づく色を決定
  const getScoreColor = (percentage: number): string => {
    if (percentage >= 80) return 'text-green-600';
    if (percentage >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  if (!isAuthenticated) {
    return (
      <div className="max-w-4xl mx-auto space-y-8">
        <Card>
          <CardContent className="py-8 text-center">
            <p className="text-gray-500 mb-4">ログインが必要です</p>
            <Button onClick={() => navigate('/login')}>
              ログインページへ
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* ヘッダー */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">完了したクイズ</h1>
          <p className="mt-1 text-lg text-gray-600">
            {filteredAndSortedQuizzes.length}件のクイズが見つかりました（全{completedQuizzes.length}件中）
          </p>
        </div>
        <Button 
          variant="secondary" 
          onClick={() => navigate('/')}
        >
          ダッシュボードに戻る
        </Button>
      </div>

      {/* 絞り込み・ソート機能 */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-lg">絞り込み・ソート設定</CardTitle>
            <Button variant="outline" size="sm" onClick={resetFilters}>
              フィルターをリセット
            </Button>
          </div>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">
            {/* カテゴリー絞り込み */}
            <div className="space-y-2">
              <label htmlFor="filterCategory" className="text-sm font-medium text-gray-700">
                カテゴリー:
              </label>
              <select
                id="filterCategory"
                value={filterCategory}
                onChange={(e) => setFilterCategory(e.target.value)}
                className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">すべて</option>
                {availableCategories.map((category) => (
                  <option key={category} value={category}>
                    {category}
                  </option>
                ))}
              </select>
            </div>

            {/* 難易度絞り込み */}
            <div className="space-y-2">
              <label htmlFor="filterDifficulty" className="text-sm font-medium text-gray-700">
                難易度:
              </label>
              <select
                id="filterDifficulty"
                value={filterDifficulty}
                onChange={(e) => setFilterDifficulty(e.target.value)}
                className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">すべて</option>
                {availableDifficulties.map((difficulty) => (
                  <option key={difficulty} value={difficulty}>
                    {difficulty}
                  </option>
                ))}
              </select>
            </div>

            {/* 期間絞り込み */}
            <div className="space-y-2">
              <label htmlFor="filterPeriod" className="text-sm font-medium text-gray-700">
                期間:
              </label>
              <select
                id="filterPeriod"
                value={filterPeriod}
                onChange={(e) => setFilterPeriod(e.target.value)}
                className="w-full border border-gray-300 rounded-md px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">すべて</option>
                <option value="week">過去1週間</option>
                <option value="month">過去1ヶ月</option>
                <option value="quarter">過去3ヶ月</option>
              </select>
            </div>

            {/* スコア範囲絞り込み */}
            <div className="space-y-2">
              <label htmlFor="filterScoreMin" className="text-sm font-medium text-gray-700">
                最低スコア:
              </label>
              <input
                type="range"
                id="filterScoreMin"
                min="0"
                max="100"
                value={filterScoreMin}
                onChange={(e) => setFilterScoreMin(Number(e.target.value))}
                className="w-full"
              />
              <div className="text-xs text-gray-500">{filterScoreMin}%</div>
            </div>

            <div className="space-y-2">
              <label htmlFor="filterScoreMax" className="text-sm font-medium text-gray-700">
                最高スコア:
              </label>
              <input
                type="range"
                id="filterScoreMax"
                min="0"
                max="100"
                value={filterScoreMax}
                onChange={(e) => setFilterScoreMax(Number(e.target.value))}
                className="w-full"
              />
              <div className="text-xs text-gray-500">{filterScoreMax}%</div>
            </div>
          </div>

          {/* ソート機能 */}
          <div className="border-t pt-4">
            <div className="flex flex-wrap gap-4">
              <div className="flex items-center space-x-2">
                <label htmlFor="sortBy" className="text-sm font-medium text-gray-700">
                  並び順:
                </label>
                <select
                  id="sortBy"
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value as 'date' | 'score' | 'category')}
                  className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="date">完了日時</option>
                  <option value="score">スコア</option>
                  <option value="category">カテゴリー</option>
                </select>
              </div>
              <div className="flex items-center space-x-2">
                <label htmlFor="sortOrder" className="text-sm font-medium text-gray-700">
                  順序:
                </label>
                <select
                  id="sortOrder"
                  value={sortOrder}
                  onChange={(e) => setSortOrder(e.target.value as 'asc' | 'desc')}
                  className="border border-gray-300 rounded-md px-3 py-1 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  <option value="desc">降順</option>
                  <option value="asc">昇順</option>
                </select>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* 完了クイズ一覧 */}
      <div>
        {loading ? (
          <div className="grid gap-4">
            {[...Array(5)].map((_, index) => (
              <Card key={index} className="animate-pulse">
                <CardContent className="py-6">
                  <div className="flex items-center justify-between">
                    <div className="space-y-2">
                      <div className="h-6 bg-gray-200 rounded w-48"></div>
                      <div className="h-4 bg-gray-200 rounded w-32"></div>
                      <div className="h-4 bg-gray-200 rounded w-24"></div>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="h-10 bg-gray-200 rounded w-16"></div>
                      <div className="h-8 bg-gray-200 rounded w-20"></div>
                      <div className="h-8 bg-gray-200 rounded w-20"></div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : error ? (
          <Card>
            <CardContent className="py-8 text-center">
              <p className="text-red-500 mb-4">{error}</p>
              <Button onClick={fetchCompletedQuizzes} variant="secondary">
                再試行
              </Button>
            </CardContent>
          </Card>
        ) : filteredAndSortedQuizzes.length === 0 ? (
          <Card>
            <CardContent className="py-8 text-center">
              <p className="text-gray-500 mb-4">
                {completedQuizzes.length === 0 
                  ? '完了したクイズがありません' 
                  : '絞り込み条件に一致するクイズがありません'
                }
              </p>
              {completedQuizzes.length === 0 ? (
                <Button onClick={() => navigate('/')}>
                  クイズを始める
                </Button>
              ) : (
                <Button onClick={resetFilters} variant="secondary">
                  フィルターをリセット
                </Button>
              )}
            </CardContent>
          </Card>
        ) : (
          <div className="space-y-4">
            {filteredAndSortedQuizzes.map((quiz) => (
              <Card key={quiz.id} className="hover:shadow-md transition-shadow">
                <CardContent className="py-6">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                       <div className="mb-2">
                         <h3 className="text-lg font-semibold text-gray-900">
                           {quiz.quiz_title}
                         </h3>
                       </div>
                      <div className="space-y-1 text-sm text-gray-600">
                        <p>
                          <span className="font-medium">カテゴリー:</span> {quiz.category_name}
                        </p>
                        <p>
                          <span className="font-medium">難易度:</span> {quiz.difficulty_name}
                        </p>
                        <p>
                          <span className="font-medium">完了日時:</span>{' '}
                          {new Date(quiz.completed_at).toLocaleString('ja-JP')}
                        </p>
                        <p>
                          <span className="font-medium">所要時間:</span>{' '}
                          {Math.floor(quiz.time_taken / 60)}分{quiz.time_taken % 60}秒
                        </p>
                      </div>
                    </div>
                    <div className="flex items-center space-x-4">
                      {/* スコア表示 */}
                      <div className="text-center">
                        <p className={`text-2xl font-bold ${getScoreColor(quiz.percentage)}`}>
                          {Math.round(quiz.percentage)}%
                        </p>
                        <p className="text-xs text-gray-500">
                          {quiz.score}/{quiz.total_possible}
                        </p>
                      </div>
                      
                      {/* アクションボタン */}
                      <div className="flex flex-col space-y-2">
                        <Button
                          size="sm"
                          variant="secondary"
                          onClick={() => handleReviewQuiz(quiz)}
                        >
                          復習する
                        </Button>
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleViewDetails(quiz)}
                        >
                          詳細表示
                        </Button>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        )}
      </div>
    </div>
  );
} 