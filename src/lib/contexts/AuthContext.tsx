import React, { createContext, useState, useEffect, useContext } from 'react';
import { 
  login as loginApi, 
  logout as logoutApi, 
  getCurrentUser, 
  refreshToken, 
  verifyToken,
  LoginCredentials,
  User
} from '../api/services/authService';

interface AuthContextType {
  user: User | null;
  loading: boolean;
  error: string | null;
  login: (credentials: LoginCredentials) => Promise<boolean>;
  logout: () => void;
  isAuthenticated: boolean;
}

// コンテキストの作成
const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
  error: null,
  login: async () => false,
  logout: () => {},
  isAuthenticated: false,
});

// カスタムフック
export const useAuth = () => useContext(AuthContext);

interface AuthProviderProps {
  children: React.ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  // 初期化時にトークンの検証とユーザー情報の取得
  useEffect(() => {
    const initAuth = async () => {
      setLoading(true);
      try {
        const isValid = await verifyToken();
        
        if (isValid) {
          const userData = await getCurrentUser();
          if (userData) {
            setUser(userData);
            setIsAuthenticated(true);
          } else {
            // トークンは有効だがユーザー情報が取得できない場合
            await refreshToken(); // トークンの更新を試みる
            const refreshedUserData = await getCurrentUser();
            if (refreshedUserData) {
              setUser(refreshedUserData);
              setIsAuthenticated(true);
            } else {
              // それでも取得できない場合はログアウト
              logout();
            }
          }
        } else {
          // トークンが無効な場合
          logout();
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
  }, []);

  // ログイン処理
  const login = async (credentials: LoginCredentials): Promise<boolean> => {
    setLoading(true);
    setError(null);
    
    try {
      await loginApi(credentials);
      const userData = await getCurrentUser();
      
      if (userData) {
        setUser(userData);
        setIsAuthenticated(true);
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
  const logout = () => {
    logoutApi();
    setUser(null);
    setIsAuthenticated(false);
  };

  // コンテキストの値
  const value = {
    user,
    loading,
    error,
    login,
    logout,
    isAuthenticated,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}; 