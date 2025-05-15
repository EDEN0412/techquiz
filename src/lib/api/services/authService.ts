import { AxiosError } from 'axios';
import apiClient from '../client';
import { saveTokens, removeTokens, getRefreshToken, getAccessToken } from '../token';

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username: string;
  password: string;
  password2: string;
  email: string;
  first_name: string;
  last_name: string;
}

export interface TokenResponse {
  access: string;
  refresh: string;
}

export interface User {
  id: number;
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  profile?: {
    bio?: string;
    date_of_birth?: string;
    avatar_url?: string;
  };
}

/**
 * ユーザー登録
 */
export const register = async (data: RegisterData): Promise<User> => {
  const response = await apiClient.post<User>('/users/register/', data);
  return response.data;
};

/**
 * ログイン
 */
export const login = async (credentials: LoginCredentials): Promise<TokenResponse> => {
  const response = await apiClient.post<TokenResponse>('/users/token/', credentials);
  
  // トークンを保存
  if (response.data.access && response.data.refresh) {
    saveTokens(response.data.access, response.data.refresh);
  }
  
  return response.data;
};

/**
 * ログアウト
 */
export const logout = (): void => {
  removeTokens();
};

/**
 * トークンのリフレッシュ
 */
export const refreshToken = async (): Promise<string | null> => {
  const refresh = getRefreshToken();
  if (!refresh) return null;
  
  try {
    const response = await apiClient.post<{ access: string }>('/users/token/refresh/', { refresh });
    saveTokens(response.data.access, refresh);
    return response.data.access;
  } catch (error) {
    const axiosError = error as AxiosError;
    // 401エラーが発生した場合はトークンが無効なので削除
    if (axiosError.response?.status === 401) {
      removeTokens();
    }
    return null;
  }
};

/**
 * 現在のユーザー情報を取得
 */
export const getCurrentUser = async (): Promise<User | null> => {
  try {
    const response = await apiClient.get<User>('/users/users/me/');
    return response.data;
  } catch (error) {
    return null;
  }
};

/**
 * トークンの有効性を検証
 */
export const verifyToken = async (): Promise<boolean> => {
  const token = getAccessToken();
  if (!token) return false;
  
  try {
    await apiClient.post('/users/token/verify/', { token });
    return true;
  } catch {
    return false;
  }
}; 