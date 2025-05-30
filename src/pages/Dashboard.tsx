import { Button } from '../components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { useNavigate } from 'react-router-dom';
import { useUserStats } from '../hooks/useUserStats';
import { useRecentActivities } from '../hooks/useRecentActivities';
import { useCategories } from '../hooks/useCategories';
import { enrichCategoriesWithIcons } from '../lib/utils/categoryIcons';

export function Dashboard() {
  const navigate = useNavigate();
  const { stats, loading: statsLoading, error: statsError } = useUserStats();
  const { activities, loading: activitiesLoading, error: activitiesError } = useRecentActivities(3);
  const { categories: rawCategories, loading: categoriesLoading, error: categoriesError, retry: retryCategories } = useCategories();

  // カテゴリーにアイコン情報を追加
  const categories = enrichCategoriesWithIcons(rawCategories);

  const handleStartQuiz = (categorySlug: string) => {
    navigate(`/quiz/${categorySlug}/difficulty`);
  };

  // 統計情報の表示値（未認証時は '-' を表示）
  const totalQuizzes = stats?.total_quizzes_completed ?? '-';
  const averageScore = stats?.overall_avg_score ? Math.round(stats.overall_avg_score) : '-';

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">おかえりなさい！</h1>
          <p className="mt-1 text-lg text-gray-600">技術力を試してみましょう</p>
        </div>
        <div className="flex items-center space-x-4 rounded-lg bg-white p-4 shadow-sm">
          <div className="text-center">
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
                    <Button variant="secondary" size="sm">
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