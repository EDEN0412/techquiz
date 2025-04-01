/**
 * API関連の型定義
 */

// 認証関連
export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  password_confirm: string;
}

export interface AuthResponse {
  access: string;
  refresh: string;
  user: UserProfile;
}

export interface TokenRefreshRequest {
  refresh: string;
}

export interface TokenRefreshResponse {
  access: string;
  refresh: string;
}

export interface PasswordResetRequest {
  email: string;
}

export interface PasswordResetConfirmRequest {
  uid: string;
  token: string;
  new_password: string;
  new_password_confirm: string;
}

// ユーザー関連
export interface UserProfile {
  id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  date_joined: string;
}

// クイズ関連
export interface Category {
  id: number;
  name: string;
  description: string;
  icon?: string;
}

export interface Difficulty {
  id: number;
  name: string;
  level: 'beginner' | 'intermediate' | 'advanced';
}

export interface QuizQuestion {
  id: number;
  text: string;
  explanation?: string;
  category: number;
  difficulty: number;
  type: 'multiple_choice' | 'text_input';
  options?: QuizOption[];
}

export interface QuizOption {
  id: number;
  text: string;
  is_correct: boolean;
}

export interface QuizSubmission {
  question_id: number;
  answer_id?: number;
  text_answer?: string;
}

export interface QuizResult {
  total_questions: number;
  correct_answers: number;
  score: number;
  quiz_id: number;
  completed_at: string;
  questions: QuizQuestionResult[];
}

export interface QuizQuestionResult {
  question_id: number;
  question_text: string;
  user_answer: string;
  correct_answer: string;
  is_correct: boolean;
  explanation?: string;
}

// API共通レスポンス
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  status: 'success' | 'error';
}

// ページネーション
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
} 