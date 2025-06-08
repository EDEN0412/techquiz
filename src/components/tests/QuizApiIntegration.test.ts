import { vi } from 'vitest';
import { QuizService } from '../../lib/api/services/quiz.service';
import { AxiosResponse } from 'axios';

// APIクライアントをモック
vi.mock('../../lib/api/client', () => {
  return {
    default: {
      get: vi.fn(),
      post: vi.fn(),
      put: vi.fn(),
      delete: vi.fn(),
      patch: vi.fn()
    }
  };
});

// モックAPIをインポート
import api from '../../lib/api/client';
const mockApi = api as jest.Mocked<typeof api>;

// モックAPIデータ
const mockCategories = [
  {
    id: 1,
    name: 'Python',
    slug: 'python',
    description: 'Python programming language',
    display_order: 1,
    is_active: true,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 2,
    name: 'JavaScript',
    slug: 'javascript',
    description: 'JavaScript programming language',
    display_order: 2,
    is_active: true,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  },
];

const mockDifficulties = [
  {
    id: 1,
    name: 'Beginner',
    slug: 'beginner',
    description: 'Beginner level',
    level: 1,
    point_multiplier: 1.0,
    time_limit: 300,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  },
  {
    id: 2,
    name: 'Intermediate',
    slug: 'intermediate',
    description: 'Intermediate level',
    level: 2,
    point_multiplier: 1.5,
    time_limit: 600,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  },
];

const mockQuizzes = [
  {
    id: 1,
    title: 'Python Basics',
    description: 'Basic Python programming concepts',
    category: 1,
    difficulty: 1,
    time_limit: 30,
    pass_score: 60,
    is_active: true,
    created_at: '2024-01-01T00:00:00Z',
    updated_at: '2024-01-01T00:00:00Z',
  },
];

// モックAxiosResponseの作成ヘルパー
function createMockAxiosResponse<T>(data: T): AxiosResponse<T> {
  return {
    data,
    status: 200,
    statusText: 'OK',
    headers: {},
    config: {} as any,
  };
}

describe('QuizService Integration Tests', () => {
  let quizService: QuizService;

  beforeEach(() => {
    quizService = new QuizService();
    vi.clearAllMocks();
  });

  // カテゴリ一覧取得のテスト
  test('getCategories should fetch categories from the API', async () => {
    // モックレスポンスを設定
    mockApi.get.mockResolvedValueOnce(createMockAxiosResponse(mockCategories));

    // APIの呼び出し
    const result = await quizService.getCategories();

    // 期待される結果の検証
    expect(mockApi.get).toHaveBeenCalledWith('/quiz/categories/');
    expect(result).toEqual(mockCategories);
    expect(result.length).toBe(2);
    expect(result[0].name).toBe('Python');
  });

  // 難易度一覧取得のテスト
  test('getDifficultyLevels should fetch difficulty levels from the API', async () => {
    // モックレスポンスを設定
    mockApi.get.mockResolvedValueOnce(createMockAxiosResponse(mockDifficulties));

    // APIの呼び出し
    const result = await quizService.getDifficultyLevels();

    // 期待される結果の検証
    expect(mockApi.get).toHaveBeenCalledWith('/quiz/difficulty-levels/');
    expect(result).toEqual(mockDifficulties);
    expect(result.length).toBe(2);
    expect(result[0].name).toBe('Beginner');
  });

  // カテゴリと難易度でフィルタリングされたクイズ取得のテスト
  test('getQuizzesByCategoryAndDifficulty should fetch filtered quizzes', async () => {
    // モックレスポンスを設定
    mockApi.get.mockResolvedValueOnce(createMockAxiosResponse(mockQuizzes));

    // APIの呼び出し
    const result = await quizService.getQuizzesByCategoryAndDifficulty(1, 1);

    // 期待される結果の検証
    expect(mockApi.get).toHaveBeenCalledWith('/quiz/filter/quizzes/1/1/');
    expect(result).toEqual(mockQuizzes);
    expect(result.length).toBe(1);
    expect(result[0].title).toBe('Python Basics');
  });

  // クイズ結果保存のテスト
  test('saveQuizResult should save the quiz result to the API', async () => {
    // モックレスポンスを設定（QuizResultResponse型に適合）
    const mockResultResponse = {
      id: 1,
      user: 1,
      username: 'testuser',
      quiz: 1,
      quiz_title: 'Python Basics',
      category_name: 'Python',
      difficulty_name: 'Beginner',
      score: 8,
      total_possible: 10,
      percentage: 80.0,
      time_taken: 300,
      passed: true,
      completed_at: '2024-01-01T00:00:00Z',
      created_at: '2024-01-01T00:00:00Z',
      updated_at: '2024-01-01T00:00:00Z',
    };
    mockApi.post.mockResolvedValueOnce(createMockAxiosResponse(mockResultResponse));

    // APIの呼び出し（QuizResultRequest型のプロパティを使用）
    const result = await quizService.saveQuizResult({
      quiz: 1,
      score: 8,
      total_possible: 10,
      percentage: 80.0,
      time_taken: 300,
    });

    // 期待される結果の検証
    expect(mockApi.post).toHaveBeenCalledWith('/quiz/quiz-results/', {
      quiz: 1,
      score: 8,
      total_possible: 10,
      percentage: 80.0,
      time_taken: 300,
    });
    expect(result).toEqual(mockResultResponse);
    expect(result.score).toBe(8);
    expect(result.percentage).toBe(80.0);
  });

  // エラーハンドリングのテスト
  test('API error should be handled properly', async () => {
    // モックエラーを設定
    const mockError = new Error('Network Error');
    mockApi.get.mockRejectedValueOnce(mockError);

    // エラーのテスト
    await expect(quizService.getCategories()).rejects.toThrow('Network Error');
    expect(mockApi.get).toHaveBeenCalledWith('/quiz/categories/');
  });
}); 