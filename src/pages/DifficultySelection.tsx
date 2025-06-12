import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { ArrowLeft, Star, Trophy } from 'lucide-react';
import { Category, Difficulty, Quiz } from '../lib/api/types';
import { getCategoryIcon } from '../lib/utils/categoryIcons';
import { QuizService } from '../lib/api/services/quiz.service';

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

// 設定フラグ - APIを使用するように変更
const USE_MOCK_DATA = false;

interface QuizCardData {
  quiz: Quiz;
  difficulty: Difficulty;
}

// Django APIサービスのインスタンス
const quizService = new QuizService();

export function DifficultySelection() {
  const { categoryId } = useParams<{ categoryId: string }>();
  const navigate = useNavigate();
  
  const [category, setCategory] = useState<Category | null>(null);
  const [quizzesData, setQuizzesData] = useState<QuizCardData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      if (!categoryId) {
        setError('カテゴリーが指定されていません');
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setError(null);

        if (USE_MOCK_DATA) {
          // モックデータを使用（開発用）
          await new Promise(resolve => setTimeout(resolve, 300)); // ローディング状態をシミュレート
          
          const foundCategory = mockCategories.find(cat => cat.slug === categoryId);
          
          if (!foundCategory) {
            setError('指定されたカテゴリーが見つかりません');
            setLoading(false);
            return;
          }

          setCategory(foundCategory);

          // モックデータ使用時はクイズ一覧を定義していないため、空配列で代用
          setQuizzesData([]);
        } else {
          // Django APIからデータを取得
          
          // 1. カテゴリー一覧を取得してslugから該当するカテゴリーを見つける
          const categories = await quizService.getCategories();
          const foundCategory = categories.find(cat => cat.slug === categoryId);
          
          if (!foundCategory) {
            setError('指定されたカテゴリーが見つかりません');
            setLoading(false);
            return;
          }

          setCategory(foundCategory);

          // 2. 難易度一覧とクイズ一覧を取得
          const [difficultyLevels, quizzes] = await Promise.all([
            quizService.getDifficultyLevels(),
            quizService.getQuizzes()
          ]);

          // 3. このカテゴリーのクイズのみ抽出
          const categoryQuizzes = quizzes.filter(quiz => quiz.category === foundCategory.id);

          // 4. クイズごとに難易度データを紐付け
          const quizCardList: QuizCardData[] = categoryQuizzes.map(quiz => {
            const diff = difficultyLevels.find(d => d.id === quiz.difficulty)!;
            return { quiz, difficulty: diff };
          }).sort((a, b) => a.difficulty.level - b.difficulty.level);

          setQuizzesData(quizCardList);
        }
      } catch (err) {
        console.error('データの取得に失敗しました:', err);
        
        // API失敗時はモックデータにフォールバック
        if (!USE_MOCK_DATA) {
          console.log('APIが失敗したため、モックデータを使用します');
          const foundCategory = mockCategories.find(cat => cat.slug === categoryId);
          if (foundCategory) {
            setCategory(foundCategory);
            // モックデータ使用時はクイズ一覧を定義していないため、空配列で代用
            setQuizzesData([]);
          } else {
            setError('指定されたカテゴリーが見つかりません');
          }
        } else {
          setError('データの取得に失敗しました。再試行してください。');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [categoryId]);

  const handleStartQuiz = (quizData: QuizCardData) => {
    const { quiz, difficulty } = quizData;
    // 既存の QuizPage は categoryId と difficultyId で問題を取得するため、
    // クイズIDはクエリパラメータで渡す
    navigate(`/quiz/${quiz.category}/${difficulty.id}/start?quizId=${quiz.id}`);
  };

  const handleBack = () => {
    navigate('/');
  };

  const getDifficultyColor = (level: number) => {
    switch (level) {
      case 1:
        return {
          color: 'text-green-600',
          bgColor: 'bg-green-50',
          borderColor: 'border-green-200',
        };
      case 2:
        return {
          color: 'text-yellow-600',
          bgColor: 'bg-yellow-50',
          borderColor: 'border-yellow-200',
        };
      case 3:
        return {
          color: 'text-red-600',
          bgColor: 'bg-red-50',
          borderColor: 'border-red-200',
        };
      default:
        return {
          color: 'text-blue-600',
          bgColor: 'bg-blue-50',
          borderColor: 'border-blue-200',
        };
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center space-x-4">
          <div className="h-10 w-24 bg-gray-200 rounded animate-pulse"></div>
        </div>
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded mb-4"></div>
          <div className="h-4 bg-gray-200 rounded mb-8"></div>
        </div>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {[...Array(3)].map((_, index) => (
            <Card key={index} className="animate-pulse">
              <CardHeader>
                <div className="h-6 bg-gray-200 rounded mb-2"></div>
                <div className="h-4 bg-gray-200 rounded"></div>
              </CardHeader>
              <CardContent>
                <div className="space-y-2 mb-4">
                  <div className="h-4 bg-gray-200 rounded"></div>
                  <div className="h-4 bg-gray-200 rounded"></div>
                </div>
                <div className="h-10 bg-gray-200 rounded"></div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        <Button onClick={handleBack} variant="secondary" className="flex items-center space-x-2">
          <ArrowLeft className="h-4 w-4" />
          <span>戻る</span>
        </Button>
        <Card>
          <CardContent className="py-12 text-center">
            <p className="text-red-500 text-lg mb-4">{error}</p>
            <Button onClick={() => window.location.reload()}>
              再試行
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!category) {
    return null;
  }

  const categoryIcon = getCategoryIcon(category);
  const Icon = categoryIcon.icon;

  return (
    <div className="space-y-6">
      {/* Back Button */}
      <Button onClick={handleBack} variant="secondary" className="flex items-center space-x-2">
        <ArrowLeft className="h-4 w-4" />
        <span>戻る</span>
      </Button>

      {/* Category Header */}
      <div className="flex items-center space-x-4">
        <div className={`flex h-16 w-16 items-center justify-center rounded-xl ${categoryIcon.bgColor}`}>
          <Icon className={`h-10 w-10 ${categoryIcon.color}`} />
        </div>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">{category.name}</h1>
          <p className="text-lg text-gray-600">{category.description}</p>
        </div>
      </div>

      {/* Difficulty Selection */}
      <div>
        <h2 className="mb-6 text-xl font-semibold text-gray-900">難易度を選択してください</h2>
        
        {quizzesData.length === 0 ? (
          <Card>
            <CardContent className="py-8 text-center text-gray-500">
              このカテゴリーには利用可能な難易度がありません。
            </CardContent>
          </Card>
        ) : (
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {quizzesData.map((item) => {
              const { difficulty, quiz } = item;
              const colorConfig = getDifficultyColor(difficulty.level);
              
              return (
                <Card 
                  key={quiz.id} 
                  interactive 
                  className={`group cursor-pointer border-2 ${colorConfig.borderColor} hover:shadow-lg`}
                >
                  <CardHeader className={colorConfig.bgColor}>
                    <div className="flex items-center justify-between">
                      <CardTitle className={`${colorConfig.color} flex items-center space-x-2`}>
                        <span>{quiz.title}</span>
                        <div className="flex">
                          {[...Array(difficulty.level)].map((_, i) => (
                            <Star key={i} className={`h-4 w-4 ${colorConfig.color} fill-current`} />
                          ))}
                        </div>
                      </CardTitle>
                    </div>
                    <CardDescription>{difficulty.description}</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="flex items-center justify-center text-sm text-gray-600">
                      <div className="flex items-center space-x-1">
                        <Trophy className="h-4 w-4" />
                        <span>{difficulty.point_multiplier}x ポイント</span>
                      </div>
                    </div>
                    <Button 
                      className="w-full" 
                      onClick={() => handleStartQuiz(item)}
                    >
                      開始する
                    </Button>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}