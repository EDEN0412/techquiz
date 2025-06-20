import { Button } from '../components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { useNavigate } from 'react-router-dom';
import { useUserStats } from '../hooks/useUserStats';
import { useRecentActivities } from '../hooks/useRecentActivities';
import { useCategories } from '../hooks/useCategories';
import { enrichCategoriesWithIcons } from '../lib/utils/categoryIcons';
import { useAuth } from '../lib/contexts/AuthContext';
import { ActivityHistory } from '../lib/api/types';
import { Trophy, Brain, Target, TrendingUp, BookOpen, Users, X, Info } from 'lucide-react';
import { useState, useEffect } from 'react';

export function Dashboard() {
  const navigate = useNavigate();
  const { user, isAuthenticated } = useAuth();
  const { stats, loading: statsLoading } = useUserStats();
  const { activities, loading: activitiesLoading, error: activitiesError } = useRecentActivities(3);
  const { categories: rawCategories, loading: categoriesLoading, error: categoriesError, retry: retryCategories } = useCategories();

  // アプリ概要セクションの表示状態を管理
  const [showAppOverview, setShowAppOverview] = useState(() => {
    // localStorageから設定を読み込む（デフォルトはtrue）
    const saved = localStorage.getItem('hideAppOverview');
    return saved !== 'true';
  });

  // 表示状態が変更されたらlocalStorageに保存
  useEffect(() => {
    localStorage.setItem('hideAppOverview', (!showAppOverview).toString());
  }, [showAppOverview]);

  // カテゴリーにアイコン情報を追加
  const categories = enrichCategoriesWithIcons(rawCategories);

  const handleStartQuiz = (categorySlug: string) => {
    navigate(`/quiz/${categorySlug}/difficulty`);
  };

  // 復習機能のハンドラー
  const handleReviewQuiz = (activity: ActivityHistory) => {
    // category id は activity.category に含まれている
    const categoryId = activity.category;
    navigate(`/quiz/${categoryId}/review?quizId=${activity.quiz}`);
  };

  // 完了したクイズ一覧ページへ遷移
  const handleViewCompletedQuizzes = () => {
    if (isAuthenticated) {
      navigate('/completed-quizzes');
    } else {
      navigate('/login');
    }
  };

  // 統計情報の表示値（未認証時は '-' を表示）
  const totalQuizzes = stats?.total_quizzes_completed ?? '-';
  const averageScore = stats?.overall_avg_score ? Math.round(stats.overall_avg_score) : '-';

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            {isAuthenticated && user ? `おかえりなさい、${user.username}さん！` : 'おかえりなさい！'}
          </h1>
          <p className="mt-1 text-lg text-gray-600">
            技術力を試してみましょう
            {!isAuthenticated && (
              <span className="ml-2 text-sm text-orange-600">
                （ログインすると結果が保存されます）
              </span>
            )}
          </p>
        </div>
        <div className="flex items-center space-x-4 rounded-lg bg-white p-4 shadow-sm">
          <div 
            className="text-center cursor-pointer hover:bg-gray-50 p-2 rounded-lg transition-colors"
            onClick={handleViewCompletedQuizzes}
            title="クリックして完了したクイズの一覧を表示"
          >
            <p className="text-sm text-gray-500">完了したクイズ</p>
            <p className="text-2xl font-bold text-gray-900">
              {statsLoading ? '...' : totalQuizzes}
            </p>
          </div>
          <div className="h-12 w-px bg-gray-200"></div>
          <div className="text-center">
            <p className="text-sm text-gray-500">平均スコア</p>
            <p className="text-2xl font-bold text-gray-900">
              {statsLoading ? '...' : (typeof averageScore === 'number' ? `${averageScore}%` : averageScore)}
            </p>
          </div>
        </div>
      </div>

      {/* App Overview Section */}
      {showAppOverview ? (
        <div className="bg-gradient-to-br from-blue-50 to-indigo-100 rounded-xl p-8 relative">
          {/* 閉じるボタン */}
          <button
            onClick={() => setShowAppOverview(false)}
            className="absolute top-4 right-4 text-gray-500 hover:text-gray-700 transition-colors"
            title="このセクションを非表示にする"
          >
            <X className="h-5 w-5" />
          </button>
          
          <div className="max-w-4xl mx-auto">
            <h2 className="text-2xl font-bold text-gray-900 mb-4 text-center">
              Techquizで技術力を向上させよう
            </h2>
            <p className="text-gray-700 text-center mb-8 max-w-3xl mx-auto">
              楽しみながら技術知識を身につける、プログラミング学習者向けクイズアプリ
            </p>
            
            <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
              {/* 主な機能 */}
              <div className="bg-white rounded-lg p-6 shadow-sm">
                <div className="flex items-center mb-3">
                  <div className="bg-blue-100 p-2 rounded-lg">
                    <Brain className="h-6 w-6 text-blue-600" />
                  </div>
                  <h3 className="ml-3 font-semibold text-gray-900">段階的な学習</h3>
                </div>
                <p className="text-sm text-gray-600">
                  初級・中級・上級の3段階の難易度で、自分のペースで学習を進められます。
                </p>
              </div>

              <div className="bg-white rounded-lg p-6 shadow-sm">
                <div className="flex items-center mb-3">
                  <div className="bg-green-100 p-2 rounded-lg">
                    <Target className="h-6 w-6 text-green-600" />
                  </div>
                  <h3 className="ml-3 font-semibold text-gray-900">即時フィードバック</h3>
                </div>
                <p className="text-sm text-gray-600">
                  回答後すぐに正誤判定と詳しい解説が表示され、理解を深められます。
                </p>
              </div>

              <div className="bg-white rounded-lg p-6 shadow-sm">
                <div className="flex items-center mb-3">
                  <div className="bg-purple-100 p-2 rounded-lg">
                    <TrendingUp className="h-6 w-6 text-purple-600" />
                  </div>
                  <h3 className="ml-3 font-semibold text-gray-900">進捗管理</h3>
                </div>
                <p className="text-sm text-gray-600">
                  学習履歴や統計情報で、自分の成長を可視化できます。
                  <span className="block text-xs text-gray-400 mt-1">
                    ※ 完了したクイズを押すと完了したクイズの一覧を表示
                  </span>
                </p>
              </div>

              <div className="bg-white rounded-lg p-6 shadow-sm">
                <div className="flex items-center mb-3">
                  <div className="bg-orange-100 p-2 rounded-lg">
                    <BookOpen className="h-6 w-6 text-orange-600" />
                  </div>
                  <h3 className="ml-3 font-semibold text-gray-900">幅広いカテゴリー</h3>
                </div>
                <p className="text-sm text-gray-600">
                  HTML/CSS、JavaScript、Python、Git、データベースなど多様な技術分野をカバー。
                </p>
              </div>

              <div className="bg-white rounded-lg p-6 shadow-sm">
                <div className="flex items-center mb-3">
                  <div className="bg-red-100 p-2 rounded-lg">
                    <Trophy className="h-6 w-6 text-red-600" />
                  </div>
                  <h3 className="ml-3 font-semibold text-gray-900">復習機能</h3>
                </div>
                <p className="text-sm text-gray-600">
                  過去に解いたクイズを復習して、知識の定着を図れます。
                </p>
              </div>

              <div className="bg-white rounded-lg p-6 shadow-sm">
                <div className="flex items-center mb-3">
                  <div className="bg-teal-100 p-2 rounded-lg">
                    <Users className="h-6 w-6 text-teal-600" />
                  </div>
                  <h3 className="ml-3 font-semibold text-gray-900">初心者にやさしい</h3>
                </div>
                <p className="text-sm text-gray-600">
                  アウトプットが苦手な方でも、気軽に取り組める設計になっています。
                </p>
              </div>
            </div>

            <div className="mt-8 text-center">
              <p className="text-gray-700 mb-4">
                さあ、今日から技術力向上の旅を始めましょう！
              </p>
              {!isAuthenticated && (
                <Button
                  onClick={() => navigate('/signup')}
                  className="bg-indigo-600 hover:bg-indigo-700 text-white"
                >
                  無料で始める
                </Button>
              )}
            </div>
          </div>
        </div>
      ) : (
        // アプリ概要を再表示するための小さなボタン
        <div className="flex justify-end">
          <button
            onClick={() => setShowAppOverview(true)}
            className="flex items-center gap-2 text-sm text-gray-600 hover:text-gray-900 transition-colors"
          >
            <Info className="h-4 w-4" />
            Techquizについて
          </button>
        </div>
      )}

      {/* Categories Grid */}
      <div>
        <h2 className="mb-4 text-xl font-semibold text-gray-900">クイズカテゴリー</h2>
        
        {categoriesLoading ? (
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {[...Array(6)].map((_, index) => (
              <Card key={index} className="animate-pulse">
                <CardHeader>
                  <div className="mb-2 h-12 w-12 rounded-lg bg-gray-200"></div>
                  <div className="h-6 bg-gray-200 rounded"></div>
                  <div className="h-4 bg-gray-200 rounded"></div>
                </CardHeader>
                <CardContent>
                  <div className="h-10 bg-gray-200 rounded"></div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : categoriesError ? (
          <Card>
            <CardContent className="py-8 text-center">
              <p className="text-red-500 mb-4">{categoriesError}</p>
              <Button onClick={retryCategories} variant="secondary">
                再試行
              </Button>
            </CardContent>
          </Card>
        ) : categories.length === 0 ? (
          <Card>
            <CardContent className="py-8 text-center text-gray-500">
              利用可能なカテゴリーがありません。
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            {categories.map((category) => {
              const Icon = category.iconConfig.icon;
              return (
                <Card key={category.id} interactive className="group cursor-pointer">
                  <CardHeader>
                    <div className={`mb-2 flex h-12 w-12 items-center justify-center rounded-lg ${category.iconConfig.bgColor} group-hover:scale-110 transition-transform`}>
                      <Icon className={`h-8 w-8 ${category.iconConfig.color}`} />
                    </div>
                    <CardTitle>{category.name}</CardTitle>
                    <CardDescription>{category.description}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Button 
                      className="w-full" 
                      onClick={() => handleStartQuiz(category.slug)}
                    >
                      クイズを開始
                    </Button>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        )}
      </div>

      {/* Recent Activity */}
      <div>
        <h2 className="mb-4 text-xl font-semibold text-gray-900">最近の活動</h2>
        
        <Card>
          <CardContent className="divide-y divide-gray-200">
            {activitiesLoading ? (
              <div className="py-8 text-center text-gray-500">
                読み込み中...
              </div>
            ) : activitiesError ? (
              <div className="py-8 text-center">
                <p className="text-red-500 mb-4">{activitiesError}</p>
                {activitiesError.includes('ログイン') && (
                  <Button 
                    onClick={() => navigate('/login')}
                    className="bg-blue-600 hover:bg-blue-700"
                  >
                    ログインページへ
                  </Button>
                )}
              </div>
            ) : activities.length === 0 ? (
              <div className="py-8 text-center text-gray-500">
                まだ活動履歴がありません。クイズを始めてみましょう！
              </div>
            ) : (
              activities.map((activity) => (
                <div key={activity.id} className="flex items-center justify-between py-4 first:pt-0 last:pb-0">
                  <div>
                    <p className="font-medium text-gray-900">{activity.category_name || 'カテゴリ不明'}</p>
                    <p className="text-sm text-gray-500">
                      {activity.difficulty_name || '難易度不明'} • {new Date(activity.activity_date).toLocaleDateString('ja-JP')}
                    </p>
                  </div>
                  <div className="flex items-center space-x-4">
                    <div className="text-right">
                      <p className="text-lg font-semibold text-gray-900">{Math.round(activity.percentage)}%</p>
                      <p className="text-sm text-gray-500">スコア</p>
                    </div>
                    <Button 
                      variant="secondary" 
                      size="sm"
                      onClick={() => handleReviewQuiz(activity)}
                    >
                      復習する
                    </Button>
                  </div>
                </div>
              ))
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}