import React, { useState, useEffect } from 'react';
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';
import { Category, Difficulty, QuizQuestion as QuizQuestionType, QuizResultRequest } from '../lib/api/types';
import { 
  fetchCategoryFromSupabase, 
  fetchDifficultyLevelsFromSupabase,
  fetchQuestionsByCategoryAndDifficulty 
} from '../lib/api/supabase-direct';
import { QuizService } from '../lib/api/services/quiz.service';
import { useAuth } from '../lib/contexts/AuthContext';
import QuizQuestion from '../components/quiz/QuizQuestion';
import QuizResult from '../components/quiz/QuizResult';

interface QuizPageParams extends Record<string, string | undefined> {
  categoryId: string;
  difficultyId?: string;
}

interface QuizAnswer {
  questionId: number;
  answerId: number;
}

const QuizPage: React.FC = () => {
  const { categoryId, difficultyId } = useParams<QuizPageParams>();
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { user } = useAuth();

  // 復習モードの検出
  const isReviewMode = location.pathname.includes('/review');
  const quizId = searchParams.get('quizId');
  const activityId = searchParams.get('activityId');

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

        if (isReviewMode) {
          // 復習モードの処理
          if (!quizId) {
            setError('復習用のクイズIDが指定されていません');
            return;
          }

          const quizIdNum = parseInt(quizId);
          if (isNaN(quizIdNum)) {
            setError('無効なクイズIDです');
            return;
          }

          // QuizServiceを使ってクイズ詳細を取得
          const quizData = await quizService.getQuizById(quizIdNum);
          
          // カテゴリーと難易度のデータを取得
          const [categoryData, difficultyLevels] = await Promise.all([
            fetchCategoryFromSupabase(quizData.category),
            fetchDifficultyLevelsFromSupabase()
          ]);

          const difficultyData = difficultyLevels.find((d: Difficulty) => d.id === quizData.difficulty);
          if (!difficultyData) {
            throw new Error('指定された難易度が見つかりません');
          }

          // クイズの問題を取得
          const questionsData = await fetchQuestionsByCategoryAndDifficulty(
            quizData.category,
            quizData.difficulty,
            10
          );

          if (!questionsData || questionsData.length === 0) {
            throw new Error('復習用の問題が見つかりません');
          }

          setCategory(categoryData);
          setDifficulty(difficultyData);
          setQuestions(questionsData);
          setQuiz(quizData);

        } else {
          // 通常モードの処理
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
          
          // クイズデータを設定（結果保存のため）
          if (questionsData.length > 0) {
            const firstQuestion = questionsData[0];
            const quizData = {
              id: firstQuestion.quiz,
              title: `${categoryData.name} - ${difficultyData.name}`,
              category: categoryData.id,
              difficulty: difficultyData.id,
              pass_score: 70, // デフォルト値
              total_questions: questionsData.length
            };
            console.log('クイズデータを設定:', quizData);
            setQuiz(quizData);
          } else {
            console.log('問題データが空のため、クイズデータを設定できません');
          }
        }
        
        // クイズ開始時間を記録
        setStartTime(new Date());

      } catch (err) {
        console.error('クイズデータの取得に失敗しました:', err);
        setError(err instanceof Error ? err.message : 'データの取得に失敗しました');
      } finally {
        setIsLoading(false);
      }
    };

    fetchQuizData();
  }, [categoryId, difficultyId, isReviewMode, quizId]);

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
    console.log('=== クイズ完了処理開始 ===');
    console.log('現在のユーザー:', user);
    console.log('現在のクイズ:', quiz);
    console.log('復習モード:', isReviewMode);
    console.log('開始時間:', startTime);
    
    setIsQuizCompleted(true);
    setEndTime(new Date());
    
    // 認証済みユーザーかつクイズデータが存在する場合のみ結果を保存
    if (user && quiz && startTime) {
      console.log('条件を満たしているため、結果を保存します');
      await saveQuizResult();
    } else {
      console.log('結果保存の条件を満たしていません:');
      console.log('- user:', !!user);
      console.log('- quiz:', !!quiz);
      console.log('- startTime:', !!startTime);
    }
  };

  // クイズ結果保存
  const saveQuizResult = async () => {
    console.log('=== クイズ結果保存開始 ===');
    console.log('user:', user);
    console.log('quiz:', quiz);
    console.log('startTime:', startTime);
    
    if (!user || !quiz || !startTime) {
      console.warn('結果保存に必要なデータが不足しています');
      console.log('user:', !!user, 'quiz:', !!quiz, 'startTime:', !!startTime);
      return;
    }

    try {
      setIsResultSaving(true);
      console.log('保存処理開始...');
      
      const results = calculateResults();
      const currentTime = endTime || new Date();
      const timeTaken = Math.round((currentTime.getTime() - startTime.getTime()) / 1000);
      
      console.log('計算結果:', results);
      console.log('所要時間:', timeTaken, '秒');
      
      const resultData: QuizResultRequest = {
        quiz: quiz.id,
        score: results.correctAnswers,
        total_possible: results.totalQuestions,
        percentage: results.score,
        time_taken: timeTaken,
      };

      console.log('送信データ:', resultData);
      console.log('API呼び出し開始...');
      
      const savedResult = await quizService.saveQuizResult(resultData);
      console.log('API呼び出し成功:', savedResult);
      console.log('クイズ結果が保存されました:', savedResult);
      setResultSaved(true);
      console.log('結果保存完了');
      
    } catch (error) {
      console.error('クイズ結果の保存に失敗しました:', error);
      // エラーが発生しても結果画面は表示する
    } finally {
      setIsResultSaving(false);
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
        isResultSaving={isResultSaving}
        resultSaved={resultSaved}
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