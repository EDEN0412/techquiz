/**
 * API関連のエクスポート
 */

// APIクライアント
import api from './client';

// 設定
export * from './config';

// トークン管理
export * from './token';

// 型定義
export * from './types';

// サービス
import { QuizService } from './services/quiz.service';
import { AuthService } from './services/auth.service';
import { UserService } from './services/user.service';

// APIサービスのインスタンス化
const quizService = new QuizService();
const authService = new AuthService();
const userService = new UserService();

// APIクライアントとサービスをエクスポート
export {
  api,
  quizService,
  authService,
  userService
}; 