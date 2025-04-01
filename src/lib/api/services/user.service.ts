/**
 * ユーザー関連のAPIサービス
 */
import api from '../client';
import { ENDPOINTS } from '../config';
import { UserProfile, QuizResult, PaginatedResponse } from '../types';

/**
 * ユーザープロファイルの取得
 */
export const getUserProfile = async (): Promise<UserProfile> => {
  try {
    const response = await api.get<UserProfile>(ENDPOINTS.USER.PROFILE);
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * ユーザープロファイルの更新
 */
export const updateUserProfile = async (profileData: Partial<UserProfile>): Promise<UserProfile> => {
  try {
    const response = await api.patch<UserProfile>(ENDPOINTS.USER.PROFILE, profileData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * ユーザーのクイズ履歴取得
 */
export const getUserHistory = async (page = 1, limit = 10): Promise<PaginatedResponse<QuizResult>> => {
  try {
    const response = await api.get<PaginatedResponse<QuizResult>>(ENDPOINTS.USER.HISTORY, {
      params: {
        page,
        limit
      }
    });
    return response.data;
  } catch (error) {
    throw error;
  }
}; 