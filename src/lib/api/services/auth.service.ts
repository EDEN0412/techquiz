/**
 * 認証関連のAPIサービス
 */
import api from '../client';
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

export class AuthService {
  private baseUrl = '/api/v1';

  /**
   * ログイン処理
   */
  async login(credentials: LoginRequest): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>(`${this.baseUrl}/token/`, credentials);
    
    // トークンを保存
    const { access, refresh } = response.data;
    saveTokens(access, refresh);
    
    return response.data;
  }

  /**
   * 新規登録処理
   */
  async register(userData: RegisterRequest): Promise<AuthResponse> {
    const response = await api.post<AuthResponse>(`${this.baseUrl}/users/register/`, userData);
    
    // トークンを保存
    const { access, refresh } = response.data;
    saveTokens(access, refresh);
    
    return response.data;
  }

  /**
   * トークン更新処理
   */
  async refreshToken(refreshToken: string): Promise<TokenRefreshResponse> {
    const data: TokenRefreshRequest = {
      refresh: refreshToken
    };
    const response = await api.post<TokenRefreshResponse>(`${this.baseUrl}/token/refresh/`, data);
    
    // 新しいトークンを保存
    const { access, refresh } = response.data;
    saveTokens(access, refresh);
    
    return response.data;
  }

  /**
   * トークン検証
   */
  async verifyToken(token: string): Promise<boolean> {
    try {
      await api.post(`${this.baseUrl}/token/verify/`, { token });
      return true;
    } catch (error) {
      return false;
    }
  }

  /**
   * ログアウト処理
   */
  logout(): void {
    removeTokens();
  }

  /**
   * パスワードリセット要求
   */
  async requestPasswordReset(email: string): Promise<void> {
    const data: PasswordResetRequest = { email };
    await api.post(`${this.baseUrl}/users/reset-password/`, data);
  }

  /**
   * パスワードリセット確認
   */
  async confirmPasswordReset(data: PasswordResetConfirmRequest): Promise<void> {
    await api.post(`${this.baseUrl}/users/reset-password-confirm/`, data);
  }
} 