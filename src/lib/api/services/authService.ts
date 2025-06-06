import { AxiosError } from 'axios';
import api from '../client';
import { saveTokens, removeTokens, getRefreshToken, getAccessToken } from '../token';

export interface LoginCredentials {
  username: string;
  password: string;
}

export interface RegisterData {
  username:string;
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
    const response = await api.post<User>('/users/register/', data);
    return response.data;
  } catch (error) {
    const axiosError = error as AxiosError<{[key: string]: string[]}>;
    if (axiosError.response?.data) {
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
    const response = await api.post<TokenResponse>('/users/token/', credentials);
    
    if (response.data.access && response.data.refresh) {
      saveTokens(response.data.access, response.data.refresh);
    }
    
    return response.data;
  } catch (error) {
    const axiosError = error as AxiosError<{[key: string]: any}>;
    if (axiosError.response?.data) {
        const errorDetail = axiosError.response.data.detail;
        if (errorDetail) {
            throw new Error(errorDetail);
        }

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
    
    throw new Error('ログインに失敗しました。ユーザー名またはパスワードを確認してください。');
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
    const response = await api.post<{ access: string }>('/users/token/refresh/', { refresh });
    saveTokens(response.data.access, refresh);
    return response.data.access;
  } catch (error) {
    const axiosError = error as AxiosError;
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
  const token = getAccessToken();
  if (!token) return null;

  try {
    const response = await api.get<User>('/users/me/');
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
    await api.post('/users/token/verify/', { token });
    return true;
  } catch {
    return false;
  }
};
