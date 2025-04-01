/**
 * 認証関連のAPIサービス
 */
import api from '../client';
import { ENDPOINTS } from '../config';
import { saveTokens, removeTokens } from '../token';
import { 
  LoginRequest, 
  RegisterRequest, 
  AuthResponse,
  PasswordResetRequest,
  PasswordResetConfirmRequest,
  TokenRefreshRequest,
  TokenRefreshResponse
} from '../types';

/**
 * ログイン処理
 */
export const login = async (credentials: LoginRequest): Promise<AuthResponse> => {
  try {
    const response = await api.post<AuthResponse>(ENDPOINTS.AUTH.LOGIN, credentials);
    
    // トークンを保存
    const { access, refresh } = response.data;
    saveTokens(access, refresh);
    
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * 新規登録処理
 */
export const register = async (userData: RegisterRequest): Promise<AuthResponse> => {
  try {
    const response = await api.post<AuthResponse>(ENDPOINTS.AUTH.REGISTER, userData);
    
    // トークンを保存
    const { access, refresh } = response.data;
    saveTokens(access, refresh);
    
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * トークン更新処理
 */
export const refreshToken = async (refreshToken: string): Promise<TokenRefreshResponse> => {
  try {
    const data: TokenRefreshRequest = {
      refresh: refreshToken
    };
    const response = await api.post<TokenRefreshResponse>(ENDPOINTS.AUTH.REFRESH, data);
    
    // 新しいトークンを保存
    const { access, refresh } = response.data;
    saveTokens(access, refresh);
    
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * ログアウト処理
 */
export const logout = (): void => {
  removeTokens();
};

/**
 * パスワードリセット要求
 */
export const requestPasswordReset = async (email: string): Promise<void> => {
  try {
    const data: PasswordResetRequest = { email };
    await api.post(ENDPOINTS.AUTH.PASSWORD_RESET, data);
  } catch (error) {
    throw error;
  }
};

/**
 * パスワードリセット確認
 */
export const confirmPasswordReset = async (data: PasswordResetConfirmRequest): Promise<void> => {
  try {
    await api.post(ENDPOINTS.AUTH.PASSWORD_RESET_CONFIRM, data);
  } catch (error) {
    throw error;
  }
}; 