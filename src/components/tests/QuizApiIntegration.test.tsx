import { render, screen, waitFor } from '@testing-library/react';
import { vi } from 'vitest';
import { QuizService } from '../../lib/api/services/quiz.service';

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
    description: 'Python programming language',
    display_order: 1,
    is_active: true,
  },
  {
    id: 2,
    name: 'JavaScript',
    description: 'JavaScript programming language',
    display_order: 2,
    is_active: true,
  },
];

const mockDifficulties = [
  {
    id: 1,
    name: 'Beginner',
    description: 'Beginner level',
    level: 1,
  },
  {
    id: 2,
    name: 'Intermediate',
    description: 'Intermediate level',
    level: 2,
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
  },
];

describe('QuizService Integration Tests', () => {
  let quizService: QuizService;

  beforeEach(() => {
    quizService = new QuizService();
    vi.clearAllMocks();
  });

  // カテゴリ一覧取得のテスト
  test('getCategories should fetch categories from the API', async () => {
    // モックレスポンスを設定
    mockApi.get.mockResolvedValueOnce({ data: mockCategories });

    // APIの呼び出し
    const result = await quizService.getCategories();

    // 期待される結果の検証
    expect(mockApi.get).toHaveBeenCalledWith('/api/v1/quiz/categories/');
    expect(result).toEqual(mockCategories);
    expect(result.length).toBe(2);
    expect(result[0].name).toBe('Python');
  });

  // 難易度一覧取得のテスト
  test('getDifficultyLevels should fetch difficulty levels from the API', async () => {
    // モックレスポンスを設定
    mockApi.get.mockResolvedValueOnce({ data: mockDifficulties });

    // APIの呼び出し
    const result = await quizService.getDifficultyLevels();

    // 期待される結果の検証
    expect(mockApi.get).toHaveBeenCalledWith('/api/v1/quiz/difficulty-levels/');
    expect(result).toEqual(mockDifficulties);
    expect(result.length).toBe(2);
    expect(result[0].name).toBe('Beginner');
  });

  // カテゴリと難易度でフィルタリングされたクイズ取得のテスト
  test('getQuizzesByCategoryAndDifficulty should fetch filtered quizzes', async () => {
    // モックレスポンスを設定
    mockApi.get.mockResolvedValueOnce({ data: mockQuizzes });

    // APIの呼び出し
    const result = await quizService.getQuizzesByCategoryAndDifficulty(1, 1);

    // 期待される結果の検証
    expect(mockApi.get).toHaveBeenCalledWith('/api/v1/quiz/filter/quizzes/1/1/');
    expect(result).toEqual(mockQuizzes);
    expect(result.length).toBe(1);
    expect(result[0].title).toBe('Python Basics');
  });

  // クイズ結果保存のテスト
  test('saveQuizResult should save the quiz result to the API', async () => {
    // モックレスポンスを設定
    const mockResultResponse = {
      id: 1,
      quiz: 1,
      user: 1,
      score: 8,
      total_possible: 10,
      percentage: 80,
      passed: true,
      time_taken: 25,
    };
    mockApi.post.mockResolvedValueOnce({ data: mockResultResponse });

    // APIの呼び出し
    const result = await quizService.saveQuizResult({
      quiz: 1,
      score: 8,
      total_possible: 10,
      time_taken: 25,
    });

    // 期待される結果の検証
    expect(mockApi.post).toHaveBeenCalledWith('/api/v1/quiz/quiz-results/', {
      quiz: 1,
      score: 8,
      total_possible: 10,
      time_taken: 25,
    });
    expect(result).toEqual(mockResultResponse);
    expect(result.percentage).toBe(80);
    expect(result.passed).toBe(true);
  });

  // エラーハンドリングのテスト
  test('API error should be handled properly', async () => {
    // モックエラーを設定
    const mockError = new Error('Network Error');
    mockApi.get.mockRejectedValueOnce(mockError);

    // エラーのテスト
    await expect(quizService.getCategories()).rejects.toThrow('Network Error');
    expect(mockApi.get).toHaveBeenCalledWith('/api/v1/quiz/categories/');
  });
}); 