/**
 * API接続の基本設定
 */

// APIのベースURL
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

// APIのバージョン
export const API_VERSION = 'v1';

// リクエストタイムアウト設定（ミリ秒）
export const REQUEST_TIMEOUT = 30000;

// APIエンドポイント
export const ENDPOINTS = {
  // 認証関連
  AUTH: {
    LOGIN: '/auth/login/',
    REGISTER: '/auth/register/',
    REFRESH: '/auth/refresh/',
    LOGOUT: '/auth/logout/',
    PASSWORD_RESET: '/auth/password/reset/',
    PASSWORD_RESET_CONFIRM: '/auth/password/reset/confirm/',
  },
  // クイズ関連
  QUIZ: {
    CATEGORIES: '/quiz/categories/',
    QUESTIONS: '/quiz/questions/',
    SUBMIT: '/quiz/submit/',
  },
  // ユーザー関連
  USER: {
    PROFILE: '/user/profile/',
    HISTORY: '/user/history/',
  },
}; 