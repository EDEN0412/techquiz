import { AxiosError } from 'axios';
import axios from 'axios';
import { saveTokens, removeTokens, getRefreshToken, getAccessToken } from '../token';
import { API_BASE_URL } from '../config';

// 認証用のカスタムAPIクライアント
const authApi = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

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
  try {
    const response = await authApi.post<User>('/v1/users/register/', data);
    return response.data;
  } catch (error) {
    const axiosError = error as AxiosError<{[key: string]: string[]}>;
    if (axiosError.response?.data) {
      // バックエンドから返されたエラーメッセージを整形
      const errors = axiosError.response.data;
      const errorMessages: string[] = [];
      
      Object.keys(errors).forEach(key => {
        const fieldErrors = errors[key];
        if (Array.isArray(fieldErrors)) {
          fieldErrors.forEach(err => {
            errorMessages.push(`${key}: ${err}`);
          });
        }
      });
      
      if (errorMessages.length > 0) {
        throw new Error(errorMessages.join('\n'));
      }
    }
    
    throw new Error('アカウント作成に失敗しました');
  }
};

/**
 * ログイン
 */
export const login = async (credentials: LoginCredentials): Promise<TokenResponse> => {
  try {
    const response = await authApi.post<TokenResponse>('/v1/users/token/', credentials);
    
    // トークンを保存
    if (response.data.access && response.data.refresh) {
      saveTokens(response.data.access, response.data.refresh);
    }
    
    return response.data;
  } catch (error) {
    const axiosError = error as AxiosError<{[key: string]: string[]}>;
    if (axiosError.response?.data) {
      // バックエンドから返されたエラーメッセージを整形
      const errors = axiosError.response.data;
      const errorMessages: string[] = [];
      
      Object.keys(errors).forEach(key => {
        const fieldErrors = errors[key];
        if (Array.isArray(fieldErrors)) {
          fieldErrors.forEach(err => {
            errorMessages.push(`${key}: ${err}`);
          });
        } else if (typeof fieldErrors === 'string') {
          errorMessages.push(fieldErrors);
        }
      });
      
      if (errorMessages.length > 0) {
        throw new Error(errorMessages.join('\n'));
      }
    }
    
    throw new Error('ログインに失敗しました');
  }
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
    const response = await authApi.post<{ access: string }>('/v1/users/token/refresh/', { refresh });
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
    const token = getAccessToken();
    if (token) {
      authApi.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    }
    const response = await authApi.get<User>('/v1/users/users/me/');
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
    await authApi.post('/v1/users/token/verify/', { token });
    return true;
  } catch {
    return false;
  }
}; 