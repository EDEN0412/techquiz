import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { QuizQuestion as QuizQuestionType, Category, Difficulty } from '../lib/api/types';
import { 
  fetchCategoryFromSupabase, 
  fetchDifficultyLevelsFromSupabase,
  fetchQuestionsByCategoryAndDifficulty 
} from '../lib/api/supabase-direct';
import QuizQuestion from '../components/quiz/QuizQuestion';
import QuizResult from '../components/quiz/QuizResult';
import { useAuth } from '../lib/contexts/AuthContext';

interface QuizPageParams extends Record<string, string | undefined> {
  categoryId: string;
  difficultyId: string;
}

interface QuizAnswer {
  questionId: number;
  answerId: number;
}

const QuizPage: React.FC = () => {
  const { categoryId, difficultyId } = useParams<QuizPageParams>();
  const navigate = useNavigate();
  const { user } = useAuth();
  
  // 状態管理
  const [questions, setQuestions] = useState<QuizQuestionType[]>([]);
  const [category, setCategory] = useState<Category | null>(null);
  const [difficulty, setDifficulty] = useState<Difficulty | null>(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<QuizAnswer[]>([]);
  const [selectedAnswer, setSelectedAnswer] = useState<number | undefined>();
  const [answeredQuestions, setAnsweredQuestions] = useState<Set<number>>(new Set());
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isQuizCompleted, setIsQuizCompleted] = useState(false);

  // クイズデータの取得
  useEffect(() => {
    const fetchQuizData = async () => {
      if (!categoryId || !difficultyId) {
        setError('カテゴリーまたは難易度が指定されていません');
        return;
      }
      
      const categoryIdNum = parseInt(categoryId);
      const difficultyIdNum = parseInt(difficultyId);
      
      if (isNaN(categoryIdNum) || isNaN(difficultyIdNum)) {
        setError(`無効なパラメータです。カテゴリーID: ${categoryId}, 難易度ID: ${difficultyId}`);
        return;
      }

      try {
        setIsLoading(true);
        setError(null);

        // カテゴリー、難易度、問題を並行して取得
        const [categoryData, difficultyLevels, questionsData] = await Promise.all([
          fetchCategoryFromSupabase(categoryIdNum),
          fetchDifficultyLevelsFromSupabase(),
          fetchQuestionsByCategoryAndDifficulty(
            categoryIdNum, 
            difficultyIdNum,
            10 // 最大10問
          )
        ]);

        // 難易度データから該当するものを探す
        const difficultyData = difficultyLevels.find((d: Difficulty) => d.id === difficultyIdNum);
        
        if (!difficultyData) {
          throw new Error('指定された難易度が見つかりません');
        }

        if (!questionsData || questionsData.length === 0) {
          throw new Error('この組み合わせのクイズ問題が見つかりません');
        }

        setCategory(categoryData);
        setDifficulty(difficultyData);
        setQuestions(questionsData);

      } catch (err) {
        console.error('クイズデータの取得に失敗しました:', err);
        setError(err instanceof Error ? err.message : 'データの取得に失敗しました');
      } finally {
        setIsLoading(false);
      }
    };

    fetchQuizData();
  }, [categoryId, difficultyId]);

  // 現在の問題が変わったときに選択答えをリセット
  useEffect(() => {
    const currentQuestionId = questions[currentQuestionIndex]?.id;
    if (currentQuestionId) {
      const existingAnswer = answers.find(a => a.questionId === currentQuestionId);
      setSelectedAnswer(existingAnswer?.answerId);
    }
  }, [currentQuestionIndex, questions, answers]);

  // 回答選択の処理
  const handleAnswerSelect = (answerId: number) => {
    setSelectedAnswer(answerId);
  };

  // 回答確定の処理
  const handleAnswerSubmit = () => {
    if (!selectedAnswer) return;

    const currentQuestion = questions[currentQuestionIndex];
    if (!currentQuestion) return;

    // 回答を記録
    const newAnswer: QuizAnswer = {
      questionId: currentQuestion.id,
      answerId: selectedAnswer
    };

    setAnswers(prev => {
      const filtered = prev.filter(a => a.questionId !== currentQuestion.id);
      return [...filtered, newAnswer];
    });

    // 回答済み問題に追加
    setAnsweredQuestions(prev => new Set([...prev, currentQuestion.id]));
  };

  // 次の問題への移動
  const handleNextQuestion = () => {
    if (currentQuestionIndex < questions.length - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    } else {
      // クイズ完了
      setIsQuizCompleted(true);
    }
  };

  // 前の問題への移動
  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
    }
  };

  // ホームに戻る
  const handleBackToHome = () => {
    navigate('/');
  };

  // クイズを再実行
  const handleRetryQuiz = () => {
    setCurrentQuestionIndex(0);
    setAnswers([]);
    setSelectedAnswer(undefined);
    setAnsweredQuestions(new Set());
    setIsQuizCompleted(false);
  };

  // 結果計算
  const calculateResults = () => {
    const questionResults = questions.map(question => {
      const userAnswer = answers.find(a => a.questionId === question.id);
      const isCorrect = userAnswer?.answerId === question.answers.find(a => a.is_correct)?.id;
      
      return {
        question: question,
        selectedAnswerId: userAnswer?.answerId || 0,
        isCorrect: isCorrect || false,
      };
    });

    const correctCount = questionResults.filter(r => r.isCorrect).length;

    return {
      totalQuestions: questions.length,
      correctAnswers: correctCount,
      score: Math.round((correctCount / questions.length) * 100),
      questions: questionResults
    };
  };

  // ローディング状態
  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">クイズを読み込んでいます...</p>
        </div>
      </div>
    );
  }

  // エラー状態
  if (error) {
    return (
      <div className="max-w-md mx-auto text-center py-12">
        <div className="bg-red-50 border border-red-200 rounded-lg p-6">
          <h2 className="text-xl font-bold text-red-900 mb-2">エラーが発生しました</h2>
          <p className="text-red-700 mb-4">{error}</p>
          <button
            onClick={handleBackToHome}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            ホームに戻る
          </button>
        </div>
      </div>
    );
  }

  // クイズ完了後は結果画面を表示
  if (isQuizCompleted) {
    const results = calculateResults();
    return (
      <QuizResult
        resultData={results}
        onRestartQuiz={handleRetryQuiz}
        onGoHome={handleBackToHome}
        quizTitle={`${category?.name || ''} - ${difficulty?.name || ''}`}
      />
    );
  }

  // 問題が存在しない場合
  if (questions.length === 0) {
    return (
      <div className="max-w-md mx-auto text-center py-12">
        <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6">
          <h2 className="text-xl font-bold text-yellow-900 mb-2">問題が見つかりません</h2>
          <p className="text-yellow-700 mb-4">
            選択されたカテゴリーと難易度の組み合わせには、まだ問題が登録されていません。
          </p>
          <button
            onClick={handleBackToHome}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
          >
            ホームに戻る
          </button>
        </div>
      </div>
    );
  }

  const currentQuestion = questions[currentQuestionIndex];
  const isAnswered = answeredQuestions.has(currentQuestion.id);

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      {/* ヘッダー情報 */}
      <div className="max-w-4xl mx-auto mb-6 px-6">
        <div className="bg-white rounded-lg shadow-sm p-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                {category?.name} - {difficulty?.name}
              </h1>

            </div>
            <button
              onClick={handleBackToHome}
              className="px-4 py-2 bg-gray-500 text-white rounded-lg hover:bg-gray-600"
            >
              ホームに戻る
            </button>
          </div>
        </div>
      </div>

      {/* クイズ問題 */}
      <QuizQuestion
        question={currentQuestion}
        currentQuestionNumber={currentQuestionIndex + 1}
        totalQuestions={questions.length}
        selectedAnswer={selectedAnswer}
        onAnswerSelect={handleAnswerSelect}
        onAnswerSubmit={handleAnswerSubmit}
        onNextQuestion={handleNextQuestion}
        onPreviousQuestion={handlePreviousQuestion}
        isFirstQuestion={currentQuestionIndex === 0}
        isLastQuestion={currentQuestionIndex === questions.length - 1}
        answeredQuestionsCount={answeredQuestions.size}
        isAnswered={isAnswered}
      />
    </div>
  );
};

export default QuizPage; 