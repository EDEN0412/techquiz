/**
 * ユーザー関連のAPIサービス
 */
import api from '../client';
import { UserProfile, QuizResult, PaginatedResponse } from '../types';

export class UserService {
  private baseUrl = '/api/v1';
  
  /**
   * ユーザープロファイルの取得
   */
  async getUserProfile(): Promise<UserProfile> {
    const response = await api.get<UserProfile>(`${this.baseUrl}/users/profile/`);
    return response.data;
  }
  
  /**
   * ユーザープロファイルの更新
   */
  async updateUserProfile(profileData: Partial<UserProfile>): Promise<UserProfile> {
    const response = await api.patch<UserProfile>(`${this.baseUrl}/users/profile/`, profileData);
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
  async getUserStats(): Promise<any> {
    const response = await api.get<any>(`${this.baseUrl}/quiz/user-stats-summary/`);
    return response.data;
  }
  
  /**
   * ユーザーのカテゴリー別統計取得
   */
  async getUserStatsByCategory(categoryId: number): Promise<any> {
    const response = await api.get<any>(`${this.baseUrl}/quiz/user-statistics/`, {
      params: {
        category: categoryId
      }
    });
    return response.data;
  }
} 