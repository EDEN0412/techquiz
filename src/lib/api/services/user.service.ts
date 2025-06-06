/**
 * ユーザー関連のAPIサービス
 */
import api from '../client';
import { UserProfile, QuizResult, PaginatedResponse, UserStatistics, UserStatsSummary } from '../types';

export class UserService {
  private baseUrl = '';
  
  /**
   * ユーザー情報の取得
   */
  async getUserProfile(): Promise<UserProfile> {
    const response = await api.get<UserProfile>(`${this.baseUrl}/users/me/`);
    return response.data;
  }
  
  /**
   * ユーザー情報の更新
   */
  async updateUserProfile(profileData: Partial<UserProfile>): Promise<UserProfile> {
    const response = await api.patch<UserProfile>(`${this.baseUrl}/users/me/`, profileData);
    return response.data;
  }
  
  /**
   * ユーザーのクイズ履歴取得
   */
  async getUserHistory(page = 1, limit = 10): Promise<PaginatedResponse<QuizResult>> {
    const response = await api.get<PaginatedResponse<QuizResult>>(`${this.baseUrl}/quiz/quiz-results/`, {
      params: {
        page,
        limit
      }
    });
    return response.data;
  }
  
  /**
   * ユーザーの統計情報取得
   */
  async getUserStats(): Promise<UserStatsSummary> {
    const response = await api.get<UserStatsSummary>(`${this.baseUrl}/quiz/user-stats-summary/`);
    return response.data;
  }
  
  /**
   * ユーザーのカテゴリー別統計取得
   */
  async getUserStatsByCategory(categoryId: number): Promise<PaginatedResponse<UserStatistics>> {
    const response = await api.get<PaginatedResponse<UserStatistics>>(`${this.baseUrl}/quiz/user-statistics/`, {
      params: {
        category: categoryId
      }
    });
    return response.data;
  }
} 