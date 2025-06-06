/**
 * クイズ関連のAPIサービス
 */
import api from '../client';
import { 
  Category, 
  Difficulty, 
  QuizQuestion, 
  QuizSubmission, 
  QuizResult,
  PaginatedResponse,
  UserStatsSummary,
  ActivityHistory
} from '../types';

/**
 * クイズ関連のAPIサービス
 */
export class QuizService {
  private baseUrl = '/quiz';

  /**
   * カテゴリ一覧を取得
   */
  async getCategories(): Promise<Category[]> {
    const response = await api.get<any>(`${this.baseUrl}/categories/`);
    // ページネーション形式のレスポンスを処理
    if (response.data.results) {
      return response.data.results;
    }
    return response.data;
  }

  /**
   * 難易度一覧を取得
   */
  async getDifficultyLevels(): Promise<Difficulty[]> {
    const response = await api.get<any>(`${this.baseUrl}/difficulty-levels/`);
    // ページネーション形式のレスポンスを処理
    if (response.data.results) {
      return response.data.results;
    }
    return response.data;
  }

  /**
   * クイズ一覧を取得
   */
  async getQuizzes(): Promise<any[]> {
    const response = await api.get<any>(`${this.baseUrl}/quizzes/`);
    // ページネーション形式のレスポンスを処理
    if (response.data.results) {
      return response.data.results;
    }
    return response.data;
  }

  /**
   * 特定のカテゴリに属するクイズ一覧を取得
   */
  async getQuizzesByCategory(categoryId: number): Promise<any[]> {
    const response = await api.get<any>(`${this.baseUrl}/categories/${categoryId}/quizzes/`);
    // ページネーション形式のレスポンスを処理
    if (response.data.results) {
      return response.data.results;
    }
    return response.data;
  }

  /**
   * 特定の難易度に属するクイズ一覧を取得
   */
  async getQuizzesByDifficulty(difficultyId: number): Promise<any[]> {
    const response = await api.get<any>(`${this.baseUrl}/difficulty-levels/${difficultyId}/quizzes/`);
    // ページネーション形式のレスポンスを処理
    if (response.data.results) {
      return response.data.results;
    }
    return response.data;
  }

  /**
   * カテゴリーと難易度で絞り込んだクイズ一覧を取得
   */
  async getQuizzesByCategoryAndDifficulty(categoryId: number, difficultyId: number): Promise<any[]> {
    const response = await api.get<any>(`${this.baseUrl}/filter/quizzes/${categoryId}/${difficultyId}/`);
    // ページネーション形式のレスポンスを処理
    if (response.data.results) {
      return response.data.results;
    }
    return response.data;
  }

  /**
   * 特定のクイズの詳細を取得
   */
  async getQuiz(quizId: number): Promise<any> {
    const response = await api.get<any>(`${this.baseUrl}/quizzes/${quizId}/`);
    return response.data;
  }

  /**
   * 特定のクイズに属する問題一覧を取得
   */
  async getQuestions(quizId: number): Promise<QuizQuestion[]> {
    const response = await api.get<any>(`${this.baseUrl}/quizzes/${quizId}/questions/`);
    // ページネーション形式のレスポンスを処理
    if (response.data.results) {
      return response.data.results;
    }
    return response.data;
  }

  /**
   * クイズ結果を保存
   */
  async saveQuizResult(result: Partial<QuizResult>): Promise<QuizResult> {
    const response = await api.post<QuizResult>(`${this.baseUrl}/quiz-results/`, result);
    return response.data;
  }

  /**
   * 最近の活動履歴を取得
   */
  async getRecentActivities(limit: number = 10): Promise<ActivityHistory[]> {
    const response = await api.get<any>(`${this.baseUrl}/recent-activities/`, {
      params: { limit }
    });
    // ページネーション形式のレスポンスを処理
    if (response.data.results) {
      return response.data.results;
    }
    return response.data;
  }

  /**
   * ユーザー統計情報のサマリーを取得
   * @param params フィルタリングパラメータ（start_date, end_date, sort_by, sort_dir）
   */
  async getUserStatsSummary(params?: {
    start_date?: string;
    end_date?: string;
    sort_by?: string;
    sort_dir?: 'asc' | 'desc';
  }): Promise<UserStatsSummary> {
    const response = await api.get<UserStatsSummary>(`${this.baseUrl}/user-stats-summary/`, {
      params
    });
    return response.data;
  }

  /**
   * 特定カテゴリーの取得
   */
  async getCategory(categoryId: number): Promise<Category> {
    const response = await api.get<Category>(`${this.baseUrl}/categories/${categoryId}/`);
    return response.data;
  }

  /**
   * カテゴリーと難易度でのクイズ問題の取得
   */
  async getQuestionsByCategoryAndDifficulty(
    categoryId: number, 
    difficultyId: number,
    limit = 10
  ): Promise<QuizQuestion[]> {
    const response = await api.get<any>(`${this.baseUrl}/questions/`, {
      params: {
        category: categoryId,
        difficulty: difficultyId,
        limit: limit
      }
    });
    
    let questionsData = [];
    
    // レスポンスの形式によって適切な処理を行う
    if (response.data.results) {
      // ページネーション形式の場合
      questionsData = response.data.results;
    } else {
      // 配列形式の場合
      questionsData = response.data;
    }
    
    // 各問題に対して答えを取得し、統合する
    const questionsWithAnswers = await Promise.all(
      questionsData.map(async (question: any) => {
        try {
          const answersResponse = await api.get<any>(`${this.baseUrl}/answers/`, {
            params: { question: question.id }
          });
          
          let answers = [];
          if (answersResponse.data.results) {
            answers = answersResponse.data.results;
          } else {
            answers = answersResponse.data;
          }
          
          return {
            ...question,
            answers: answers.sort((a: any, b: any) => a.order - b.order)
          };
        } catch (error) {
          console.error(`問題ID ${question.id} の答えの取得に失敗:`, error);
          return {
            ...question,
            answers: []
          };
        }
      })
    );
    
    return questionsWithAnswers;
  }

  /**
   * クイズ回答の送信
   */
  async submitQuizAnswers(submissions: QuizSubmission[]): Promise<QuizResult> {
    const response = await api.post<QuizResult>(`${this.baseUrl}/quiz-results/`, { 
      answers: submissions 
    });
    return response.data;
  }
} 