/**
 * Django APIクライアント
 */
import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse, AxiosError } from 'axios';
import { API_BASE_URL, API_VERSION, REQUEST_TIMEOUT } from './config';
import { getAccessToken, getRefreshToken, saveTokens, removeTokens } from './token';

// APIクライアントの基本設定
const apiClient: AxiosInstance = axios.create({
  baseURL: `${API_BASE_URL}/${API_VERSION}`,
  timeout: REQUEST_TIMEOUT,
  headers: {
    'Content-Type': 'application/json',
  },
});

// リクエストインターセプター
apiClient.interceptors.request.use(
  (config) => {
    const token = getAccessToken();
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// レスポンスインターセプター
apiClient.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as AxiosRequestConfig & { _retry?: boolean };
    
    // トークン期限切れエラーの場合（401）
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        // リフレッシュトークンを使用して新しいアクセストークンを取得
        const refreshToken = getRefreshToken();
        if (!refreshToken) {
          removeTokens();
          return Promise.reject(error);
        }
        
        const response = await axios.post(`${API_BASE_URL}/${API_VERSION}/users/token/refresh/`, {
          refresh: refreshToken,
        });
        
        // 新しいトークンを保存
        const { access } = response.data;
        saveTokens(access, refreshToken);
        
        // 元のリクエストを再実行
        originalRequest.headers = {
          ...originalRequest.headers,
          Authorization: `Bearer ${access}`,
        };
        
        return apiClient(originalRequest);
      } catch (refreshError) {
        // リフレッシュに失敗した場合はログアウト
        removeTokens();
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);

/**
 * APIメソッド
 */
export const api = {
  /**
   * GETリクエスト
   */
  get: <T>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return apiClient.get<T>(url, config);
  },
  
  /**
   * POSTリクエスト
   */
  post: <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return apiClient.post<T>(url, data, config);
  },
  
  /**
   * PUTリクエスト
   */
  put: <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return apiClient.put<T>(url, data, config);
  },
  
  /**
   * PATCHリクエスト
   */
  patch: <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return apiClient.patch<T>(url, data, config);
  },
  
  /**
   * DELETEリクエスト
   */
  delete: <T>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> => {
    return apiClient.delete<T>(url, config);
  },
};

export default api; 