import React, { createContext, useState, useEffect, useContext, useCallback } from 'react';
import { 
  login as loginApi, 
  logout as logoutApi, 
  getCurrentUser, 
  refreshToken, 
  verifyToken,
  LoginCredentials,
  User
} from '../api/services/authService';
import { getAccessToken, hasValidToken } from '../api/token';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  login: (credentials: LoginCredentials) => Promise<boolean>;
  logout: () => void;
  isAuthenticated: boolean;
  onAuthChange: (callback: (isAuthenticated: boolean) => void) => () => void;
}

// コンテキストの作成
const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
  error: null,
  login: async () => false,
  logout: () => {},
  isAuthenticated: false,
  onAuthChange: () => () => {},
});

// カスタムフック
export const useAuth = () => useContext(AuthContext);

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  // 初期状態でlocalStorageからトークンの存在を確認
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(hasValidToken());
  const [authChangeCallbacks, setAuthChangeCallbacks] = useState<((isAuthenticated: boolean) => void)[]>([]);

  // 認証状態変更時のコールバック登録
  const onAuthChange = useCallback((callback: (isAuthenticated: boolean) => void) => {
    setAuthChangeCallbacks(prev => [...prev, callback]);
    
    // クリーンアップ関数を返す
    return () => {
      setAuthChangeCallbacks(prev => prev.filter(cb => cb !== callback));
    };
  }, []);

  // 認証状態が変更されたときにコールバックを実行
  useEffect(() => {
    authChangeCallbacks.forEach(callback => callback(isAuthenticated));
  }, [isAuthenticated, authChangeCallbacks]);

  // 認証状態を更新するヘルパー関数
  const updateAuthState = useCallback((userData: User | null, authenticated: boolean) => {
    setUser(userData);
    setIsAuthenticated(authenticated);
  }, []);

  // 初期化時にトークンの検証とユーザー情報の取得
  useEffect(() => {
    const initAuth = async () => {
      setLoading(true);
      setError(null);
      
      // localStorageにトークンがない場合は早期リターン
      if (!hasValidToken()) {
        updateAuthState(null, false);
        setLoading(false);
        return;
      }

      try {
        // トークンの有効性を確認
        const isValid = await verifyToken();
        
        if (isValid) {
          // トークンが有効な場合、ユーザー情報を取得
          const userData = await getCurrentUser();
          if (userData) {
            updateAuthState(userData, true);
          } else {
            // ユーザー情報が取得できない場合、トークンリフレッシュを試みる
            const newToken = await refreshToken();
            if (newToken) {
              const refreshedUserData = await getCurrentUser();
              if (refreshedUserData) {
                updateAuthState(refreshedUserData, true);
              } else {
                // リフレッシュ後もユーザー情報が取得できない場合はログアウト
                logout();
              }
            } else {
              // リフレッシュに失敗した場合はログアウト
              logout();
            }
          }
        } else {
          // トークンが無効な場合、リフレッシュを試みる
          const newToken = await refreshToken();
          if (newToken) {
            // リフレッシュ成功後、ユーザー情報を取得
            const userData = await getCurrentUser();
            if (userData) {
              updateAuthState(userData, true);
            } else {
              logout();
            }
          } else {
            // リフレッシュに失敗した場合はログアウト
            logout();
          }
        }
      } catch (err) {
        setError('認証の初期化中にエラーが発生しました');
        console.error('Auth initialization error:', err);
        logout();
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, [updateAuthState]);

  // ログイン処理
  const login = async (credentials: LoginCredentials): Promise<boolean> => {
    setLoading(true);
    setError(null);
    
    try {
      await loginApi(credentials);
      const userData = await getCurrentUser();
      
      if (userData) {
        updateAuthState(userData, true);
        return true;
      } else {
        setError('ユーザー情報の取得に失敗しました');
        return false;
      }
    } catch (err) {
      const error = err as Error;
      setError(error.message || 'ログイン中にエラーが発生しました');
      return false;
    } finally {
      setLoading(false);
    }
  };

  // ログアウト処理
  const logout = useCallback(() => {
    logoutApi();
    updateAuthState(null, false);
  }, [updateAuthState]);

  // コンテキストの値
  const value = {
    user,
    loading,
    error,
    login,
    logout,
    isAuthenticated,
    onAuthChange,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}; 