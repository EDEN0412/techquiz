import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useSearchParams, useLocation } from 'react-router-dom';
import { Category, Difficulty, QuizQuestion as QuizQuestionType, QuizResultRequest } from '../lib/api/types';
import { QuizService } from '../lib/api/services/quiz.service';
import { useAuth } from '../lib/contexts/AuthContext';
import QuizQuestion from '../components/quiz/QuizQuestion';
import QuizResult from '../components/quiz/QuizResult';

interface QuizPageParams extends Record<string, string | undefined> {
  categoryId?: string;
  difficultyId?: string;
  quizId?: string;
}

interface QuizAnswer {
  questionId: number;
  answerId: number;
}

const QuizPage: React.FC = () => {
  const { categoryId, difficultyId, quizId: routeQuizId } = useParams<QuizPageParams>();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const location = useLocation();
  const { user } = useAuth();

  // 復習モードの検出
  const isReviewMode = location.pathname.includes('/review');
  const quizIdFromUrl = routeQuizId || searchParams.get('quizId');

  // State管理
  const [questions, setQuestions] = useState<QuizQuestionType[]>([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<QuizAnswer[]>([]);
  const [selectedAnswer, setSelectedAnswer] = useState<number | undefined>();
  const [answeredQuestions, setAnsweredQuestions] = useState<Set<number>>(new Set());
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isQuizCompleted, setIsQuizCompleted] = useState(false);
  const [category, setCategory] = useState<Category | null>(null);
  const [difficulty, setDifficulty] = useState<Difficulty | null>(null);
  const [quiz, setQuiz] = useState<any | null>(null);
  const [isResultSaving, setIsResultSaving] = useState(false);
  const [resultSaved, setResultSaved] = useState(false);
  
  // 時間計測用の状態
  const [startTime, setStartTime] = useState<Date | null>(null);
  const [endTime, setEndTime] = useState<Date | null>(null);

  const quizService = new QuizService();

  // クイズデータの取得
  useEffect(() => {
    const fetchQuizData = async () => {
      try {
        setIsLoading(true);
        setError(null);

        let categoryData: Category;
        let difficultyData: Difficulty;
        let questionsData: QuizQuestionType[];
        let quizData: any;

        if (isReviewMode && quizIdFromUrl) {
          // --- 復習モード (QuizServiceを使用) ---
          const quizIdNum = parseInt(quizIdFromUrl, 10);
          quizData = await quizService.getQuizById(quizIdNum);
          
          const [cat, diffs] = await Promise.all([
            quizService.getCategory(quizData.category),
            quizService.getDifficultyLevels()
          ]);
          categoryData = cat;
          difficultyData = diffs.find(d => d.id === quizData.difficulty)!;
          questionsData = await quizService.getQuestions(quizData.id);

        } else if (categoryId && difficultyId) {
          // --- 通常モード (QuizServiceを使用) ---
          const categoryIdNum = parseInt(categoryId, 10);
          const difficultyIdNum = parseInt(difficultyId, 10);

          const [cat, diffs, quizzes] = await Promise.all([
            quizService.getCategory(categoryIdNum),
            quizService.getDifficultyLevels(),
            quizService.getQuizzesByCategoryAndDifficulty(categoryIdNum, difficultyIdNum)
          ]);
          
          categoryData = cat;
          difficultyData = diffs.find(d => d.id === difficultyIdNum)!;
          
          if (!quizzes || quizzes.length === 0) {
            throw new Error("このカテゴリーと難易度の組み合わせのクイズが見つかりません。");
          }
          quizData = quizzes[0]; // 該当する最初のクイズを使用
          questionsData = await quizService.getQuestions(quizData.id);

        } else {
          throw new Error("クイズを開始するための情報が不足しています。");
        }

        if (!difficultyData) throw new Error('難易度情報が見つかりません');
        if (!questionsData || questionsData.length === 0) throw new Error('問題が見つかりません');

        setCategory(categoryData);
        setDifficulty(difficultyData);
        setQuestions(questionsData);
        setQuiz(quizData);
        setStartTime(new Date());

      } catch (err) {
        console.error('クイズデータの取得に失敗しました:', err);
        setError(err instanceof Error ? err.message : 'データの取得に失敗しました');
      } finally {
        setIsLoading(false);
      }
    };

    fetchQuizData();
  }, [categoryId, difficultyId, isReviewMode, quizIdFromUrl]);

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
      handleQuizCompletion();
    }
  };

  // クイズ完了処理
  const handleQuizCompletion = async () => {
    setIsQuizCompleted(true);
    setEndTime(new Date());
    
    // 認証済みユーザーかつクイズデータが存在する場合のみ結果を保存
    if (user && quiz && startTime) {
      await saveQuizResult();
    }
  };

  // クイズ結果保存
  const saveQuizResult = async () => {
    if (!user || !quiz || !startTime) {
      return;
    }

    try {
      setIsResultSaving(true);
      const results = calculateResults();
      const currentTime = endTime || new Date();
      const timeTaken = Math.round((currentTime.getTime() - startTime.getTime()) / 1000);
      
      const resultData: QuizResultRequest = {
        quiz: quiz.id,
        score: results.correctAnswers,
        total_possible: results.totalQuestions,
        percentage: results.score,
        time_taken: timeTaken,
      };

      await quizService.saveQuizResult(resultData);
      setResultSaved(true);
      
    } catch (error) {
      console.error('クイズ結果の保存に失敗しました:', error);
    } finally {
      setIsResultSaving(false);
    }
  };

  // 前の問題への移動
  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev + 1);
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
    setIsResultSaving(false);
    setResultSaved(false);
    setStartTime(new Date());
    setEndTime(null);
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
      score: questions.length > 0 ? Math.round((correctCount / questions.length) * 100) : 0,
      questions: questionResults
    };
  };

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

  if (isQuizCompleted) {
    const results = calculateResults();
    return (
      <QuizResult
        resultData={results}
        onRestartQuiz={handleRetryQuiz}
        onGoHome={handleBackToHome}
        quizTitle={`${category?.name || ''} - ${difficulty?.name || ''}`}
        isResultSaving={isResultSaving}
        resultSaved={resultSaved}
      />
    );
  }

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