/**
 * クイズ関連のAPIサービス
 */
import api from '../client';
import { ENDPOINTS } from '../config';
import { 
  Category, 
  Difficulty, 
  QuizQuestion, 
  QuizSubmission, 
  QuizResult,
  PaginatedResponse
} from '../types';

/**
 * カテゴリー一覧の取得
 */
export const getCategories = async (): Promise<Category[]> => {
  try {
    const response = await api.get<PaginatedResponse<Category>>(ENDPOINTS.QUIZ.CATEGORIES);
    return response.data.results;
  } catch (error) {
    throw error;
  }
};

/**
 * 特定カテゴリーの取得
 */
export const getCategory = async (categoryId: number): Promise<Category> => {
  try {
    const response = await api.get<Category>(`${ENDPOINTS.QUIZ.CATEGORIES}${categoryId}/`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

/**
 * クイズ問題の取得
 */
export const getQuestions = async (
  categoryId: number, 
  difficultyId: number,
  limit = 10
): Promise<QuizQuestion[]> => {
  try {
    const response = await api.get<PaginatedResponse<QuizQuestion>>(
      `${ENDPOINTS.QUIZ.QUESTIONS}`, {
        params: {
          category: categoryId,
          difficulty: difficultyId,
          limit: limit
        }
      }
    );
    return response.data.results;
  } catch (error) {
    throw error;
  }
};

/**
 * クイズ回答の送信
 */
export const submitQuizAnswers = async (
  submissions: QuizSubmission[]
): Promise<QuizResult> => {
  try {
    const response = await api.post<QuizResult>(ENDPOINTS.QUIZ.SUBMIT, { answers: submissions });
    return response.data;
  } catch (error) {
    throw error;
  }
}; 