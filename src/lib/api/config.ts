/**
 * API設定
 */

// API基本URL
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000';

// APIバージョン
export const API_VERSION = 'api/v1';

// リクエストタイムアウト（ミリ秒）
export const REQUEST_TIMEOUT = 15000;
