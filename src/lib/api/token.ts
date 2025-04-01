/**
 * 認証トークンの管理
 */

// ローカルストレージのキー
const ACCESS_TOKEN_KEY = 'techquiz_access_token';
const REFRESH_TOKEN_KEY = 'techquiz_refresh_token';

/**
 * アクセストークンの取得
 */
export const getAccessToken = (): string | null => {
  return localStorage.getItem(ACCESS_TOKEN_KEY);
};

/**
 * リフレッシュトークンの取得
 */
export const getRefreshToken = (): string | null => {
  return localStorage.getItem(REFRESH_TOKEN_KEY);
};

/**
 * トークンの保存
 */
export const saveTokens = (accessToken: string, refreshToken: string): void => {
  localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
  localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken);
};

/**
 * トークンの削除（ログアウト時）
 */
export const removeTokens = (): void => {
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
};

/**
 * トークンの有効性確認（簡易チェック）
 */
export const hasValidToken = (): boolean => {
  return !!getAccessToken();
}; 