// ユーザー関連
export interface UserProfile {
  id: number;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  date_joined: string;
}

// カテゴリ関連
export interface Category {
  id: number;
  name: string;
  slug: string;
  description: string;
  is_active: boolean;
  display_order: number;
  created_at: string;
  updated_at: string;
}

// 難易度関連
export interface Difficulty {
  id: number;
  name: string;
  slug: string;
  level: number;
  description: string;
  point_multiplier: number;
  time_limit: number;  // 秒単位
  created_at: string;
  updated_at: string;
}

// クイズ関連
export interface Quiz {
  id: number;
  title: string;
  description: string;
  category: number;
  difficulty: number;
  time_limit: number;
  pass_score: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface QuizQuestion {
  id: number;
  quiz: number;
  question_text: string;
  question_type: 'multiple_choice' | 'single_choice' | 'true_false' | 'fill_blank';
  explanation?: string;
  points: number;
  order: number;
  answers: Answer[];
}

export interface Answer {
  id: number;
  question: number;
  answer_text: string;
  is_correct: boolean;
  order: number;
}

export interface QuizSubmission {
  question_id: number;
  answer_id: number;
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

// ユーザー統計情報
export interface UserStatistics {
  id: number;
  user: number;
  username: string;
  category?: number;
  category_name?: string;
  difficulty?: number;
  difficulty_name?: string;
  quizzes_completed: number;
  total_points: number;
  avg_score: number;
  highest_score: number;
  last_quiz_date?: string;
  created_at: string;
  updated_at: string;
}

// ユーザー統計情報のサマリー
export interface UserStatsSummary {
  total_quizzes_completed: number;
  total_points: number;
  overall_avg_score: number;
  categories: UserStatistics[];
  difficulties: UserStatistics[];
  recent_progress?: {
    last_quiz_date: string;
    category: string | null;
    difficulty: string | null;
    score: number;
  };
}

// 活動履歴
export interface ActivityHistory {
  id: number;
  user: number;
  username: string;
  quiz: number;
  quiz_title: string;
  category?: number;
  category_name?: string;
  difficulty?: number;
  difficulty_name?: string;
  score: number;
  percentage: number;
  activity_date: string;
  activity_type: 'quiz_completed' | 'quiz_started' | 'quiz_review' | 'achievement_earned';
  activity_type_display: string;
  created_at: string;
  updated_at: string;
}

// API共通レスポンス
export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface ApiError {
  message: string;
  status: number;
  data?: any;
}

// 認証関連
export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  first_name?: string;
  last_name?: string;
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
  token: string;
  password: string;
}

