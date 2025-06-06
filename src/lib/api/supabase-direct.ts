/**
 * Supabase直接接続クライアント（開発・テスト用）
 */
import { Difficulty, Category, QuizQuestion, Answer } from './types';

// Supabaseローカル環境の設定
const SUPABASE_URL = 'http://127.0.0.1:54321';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0';

/**
 * Supabase REST APIから難易度データを取得
 */
export async function fetchDifficultyLevelsFromSupabase(): Promise<Difficulty[]> {
  try {
    const response = await fetch(`${SUPABASE_URL}/rest/v1/quiz_difficultylevel?select=*&order=level.asc`, {
      headers: {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    // Supabaseのデータ形式をフロントエンドの型に変換
    return data.map((item: any): Difficulty => ({
      id: item.id,
      name: item.name,
      slug: item.slug,
      level: item.level,
      description: item.description || '',
      point_multiplier: item.point_multiplier,
      time_limit: item.time_limit,
      created_at: item.created_at,
      updated_at: item.updated_at,
    }));
  } catch (error) {
    console.error('Supabaseからの難易度データ取得に失敗しました:', error);
    throw error;
  }
}

/**
 * Supabase REST APIからカテゴリデータを取得
 */
export async function fetchCategoriesFromSupabase(): Promise<Category[]> {
  try {
    const response = await fetch(`${SUPABASE_URL}/rest/v1/quiz_category?select=*&order=display_order.asc`, {
      headers: {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    // Supabaseのデータ形式をフロントエンドの型に変換
    return data.map((item: any): Category => ({
      id: item.id,
      name: item.name,
      slug: item.slug,
      description: item.description || '',
      is_active: item.is_active,
      display_order: item.display_order,
      created_at: item.created_at,
      updated_at: item.updated_at,
    }));
  } catch (error) {
    console.error('Supabaseからのカテゴリデータ取得に失敗しました:', error);
    throw error;
  }
}

/**
 * 特定のカテゴリを取得
 */
export async function fetchCategoryFromSupabase(categoryId: number): Promise<Category> {
  try {
    const response = await fetch(`${SUPABASE_URL}/rest/v1/quiz_category?select=*&id=eq.${categoryId}`, {
      headers: {
        'apikey': SUPABASE_ANON_KEY,
        'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    
    if (!data || data.length === 0) {
      throw new Error('カテゴリが見つかりません');
    }

    const item = data[0];
    return {
      id: item.id,
      name: item.name,
      slug: item.slug,
      description: item.description || '',
      is_active: item.is_active,
      display_order: item.display_order,
      created_at: item.created_at,
      updated_at: item.updated_at,
    };
  } catch (error) {
    console.error('Supabaseからのカテゴリデータ取得に失敗しました:', error);
    throw error;
  }
}

/**
 * カテゴリーと難易度に基づいてクイズ問題を取得
 */
export async function fetchQuestionsByCategoryAndDifficulty(
  categoryId: number,
  difficultyId: number,
  limit: number = 10
): Promise<QuizQuestion[]> {
  try {
    // 1. クイズを取得（カテゴリーと難易度でフィルタリング）
    const quizResponse = await fetch(
      `${SUPABASE_URL}/rest/v1/quiz_quiz?select=id&category_id=eq.${categoryId}&difficulty_id=eq.${difficultyId}&is_active=eq.true`,
      {
        headers: {
          'apikey': SUPABASE_ANON_KEY,
          'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
          'Content-Type': 'application/json',
        },
      }
    );

    if (!quizResponse.ok) {
      throw new Error(`クイズ取得エラー: ${quizResponse.status}`);
    }

    const quizzes = await quizResponse.json();
    
    if (!quizzes || quizzes.length === 0) {
      return [];
    }

    const quizIds = quizzes.map((q: any) => q.id);

    // 2. 問題を取得
    const questionsResponse = await fetch(
      `${SUPABASE_URL}/rest/v1/quiz_question?select=*&quiz_id=in.(${quizIds.join(',')})&order=display_order.asc&limit=${limit}`,
      {
        headers: {
          'apikey': SUPABASE_ANON_KEY,
          'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
          'Content-Type': 'application/json',
        },
      }
    );

    if (!questionsResponse.ok) {
      throw new Error(`問題取得エラー: ${questionsResponse.status}`);
    }

    const questions = await questionsResponse.json();

    if (!questions || questions.length === 0) {
      return [];
    }

    // 3. 各問題の選択肢を取得
    const questionIds = questions.map((q: any) => q.id);
    const answersResponse = await fetch(
      `${SUPABASE_URL}/rest/v1/quiz_answer?select=*&question_id=in.(${questionIds.join(',')})`,
      {
        headers: {
          'apikey': SUPABASE_ANON_KEY,
          'Authorization': `Bearer ${SUPABASE_ANON_KEY}`,
          'Content-Type': 'application/json',
        },
      }
    );

    if (!answersResponse.ok) {
      throw new Error(`選択肢取得エラー: ${answersResponse.status}`);
    }

    const answers = await answersResponse.json();

    // 4. 問題と選択肢を結合
    const questionsWithAnswers: QuizQuestion[] = questions.map((question: any, index: number) => ({
      id: question.id,
      quiz: question.quiz_id,
      question_text: question.question_text,
      question_type: question.question_type as 'multiple_choice' | 'single_choice' | 'true_false' | 'fill_blank',
      explanation: question.explanation,
      points: question.points,
      order: question.display_order || index + 1,
      answers: (answers || [])
        .filter((answer: any) => answer.question_id === question.id)
        .map((answer: any, answerIndex: number) => ({
          id: answer.id,
          question: answer.question_id,
          answer_text: answer.answer_text,
          is_correct: answer.is_correct,
          order: answerIndex + 1 // orderカラムがないので、インデックスベースでorderを生成
        }))
        .sort((a: Answer, b: Answer) => a.order - b.order)
    }));

    return questionsWithAnswers;

  } catch (error) {
    console.error('クイズデータ取得エラー:', error);
    throw error;
  }
}
