import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import QuizQuestion from './QuizQuestion';
import QuizResult from './QuizResult';
import { QuizQuestion as QuizQuestionType } from '../../lib/api/types';

// サンプルクイズデータ
const sampleQuestions: QuizQuestionType[] = [
  {
    id: 1,
    quiz: 1,
    question_text: "HTMLでWebページの構造を定義する際、文書全体を囲む最も外側のタグは何ですか？",
    question_type: 'single_choice',
    explanation: "HTMLドキュメントのルート要素は<html>タグです。すべてのHTML要素はこのタグの中に含まれます。",
    points: 10,
    order: 1,
    answers: [
      {
        id: 1,
        question: 1,
        answer_text: "<body>",
        is_correct: false,
        order: 1
      },
      {
        id: 2,
        question: 1,
        answer_text: "<html>",
        is_correct: true,
        order: 2
      },
      {
        id: 3,
        question: 1,
        answer_text: "<head>",
        is_correct: false,
        order: 3
      },
      {
        id: 4,
        question: 1,
        answer_text: "<div>",
        is_correct: false,
        order: 4
      }
    ]
  },
  {
    id: 2,
    quiz: 1,
    question_text: "CSSでテキストの色を赤色に設定するプロパティはどれですか？",
    question_type: 'single_choice',
    explanation: "CSSでテキストの色を指定するには「color」プロパティを使用します。例：color: red;",
    points: 10,
    order: 2,
    answers: [
      {
        id: 5,
        question: 2,
        answer_text: "text-color: red;",
        is_correct: false,
        order: 1
      },
      {
        id: 6,
        question: 2,
        answer_text: "color: red;",
        is_correct: true,
        order: 2
      },
      {
        id: 7,
        question: 2,
        answer_text: "font-color: red;",
        is_correct: false,
        order: 3
      },
      {
        id: 8,
        question: 2,
        answer_text: "background: red;",
        is_correct: false,
        order: 4
      }
    ]
  },
  {
    id: 3,
    quiz: 1,
    question_text: "JavaScriptで変数を宣言する際に推奨される方法はどれですか？",
    question_type: 'single_choice',
    explanation: "ES6以降では、再代入が必要な場合は「let」、定数の場合は「const」を使用することが推奨されています。「var」は避けるべきです。",
    points: 15,
    order: 3,
    answers: [
      {
        id: 9,
        question: 3,
        answer_text: "var を使用する",
        is_correct: false,
        order: 1
      },
      {
        id: 10,
        question: 3,
        answer_text: "let または const を使用する",
        is_correct: true,
        order: 2
      },
      {
        id: 11,
        question: 3,
        answer_text: "変数宣言は不要",
        is_correct: false,
        order: 3
      },
      {
        id: 12,
        question: 3,
        answer_text: "function を使用する",
        is_correct: false,
        order: 4
      }
    ]
  }
];

const QuizQuestionDemo: React.FC = () => {
  const navigate = useNavigate();
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<{[key: number]: number}>({});
  const [answeredQuestions, setAnsweredQuestions] = useState<Set<number>>(new Set());
  const [hasStarted, setHasStarted] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);
  const [quizStartTime] = useState<Date>(new Date());

  const currentQuestion = sampleQuestions[currentQuestionIndex];
  const totalQuestions = sampleQuestions.length;
  
  // 回答済み問題数を計算
  const answeredQuestionsCount = answeredQuestions.size;

  const handleAnswerSelect = (answerId: number) => {
    setSelectedAnswers(prev => ({
      ...prev,
      [currentQuestion.id]: answerId
    }));
  };

  const handleAnswerSubmit = () => {
    setAnsweredQuestions(prev => new Set([...prev, currentQuestion.id]));
  };

  const handleStartQuiz = () => {
    setHasStarted(true);
  };

  const handleNextQuestion = () => {
    if (currentQuestionIndex < totalQuestions - 1) {
      setCurrentQuestionIndex(prev => prev + 1);
    } else {
      // クイズ完了時
      setIsCompleted(true);
    }
  };

  // 結果データを計算する関数
  const calculateResults = () => {
    const questionResults = sampleQuestions.map(question => {
      const selectedAnswerId = selectedAnswers[question.id];
      const selectedAnswer = question.answers.find(a => a.id === selectedAnswerId);
      const isCorrect = selectedAnswer?.is_correct || false;
      
      return {
        question,
        selectedAnswerId: selectedAnswerId || 0,
        isCorrect,
        timeSpent: 0 // 今回は時間計測は実装しない
      };
    });

    const correctAnswers = questionResults.filter(result => result.isCorrect).length;
    const score = Math.round((correctAnswers / totalQuestions) * 100);
    const timeSpent = Math.round((new Date().getTime() - quizStartTime.getTime()) / 1000);

    return {
      totalQuestions,
      correctAnswers,
      score,
      timeSpent,
      questions: questionResults
    };
  };

  // 結果画面でのアクション
  const handleRestartQuiz = () => {
    setCurrentQuestionIndex(0);
    setSelectedAnswers({});
    setAnsweredQuestions(new Set());
    setHasStarted(false);
    setIsCompleted(false);
  };

  const handleGoHome = () => {
    navigate('/');
  };

  // 結果画面の表示
  if (isCompleted) {
    const resultData = calculateResults();
    return (
      <QuizResult
        resultData={resultData}
        onRestartQuiz={handleRestartQuiz}
        onGoHome={handleGoHome}
        quizTitle="HTML/CSS/JavaScript クイズ"
      />
    );
  }

  const handlePreviousQuestion = () => {
    if (currentQuestionIndex > 0) {
      setCurrentQuestionIndex(prev => prev - 1);
    }
  };

  if (!hasStarted) {
    // クイズ開始前の画面
    return (
      <div className="min-h-screen bg-gray-100 py-8">
        <div className="container mx-auto px-4">
          {/* ヘッダー */}
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              HTML/CSS/JavaScript クイズ
            </h1>
            <p className="text-gray-600">
              Web開発の基礎知識をテストしてみましょう！
            </p>
          </div>

          {/* 使い方説明 */}
          <div className="max-w-4xl mx-auto mb-8">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-blue-900 mb-4">📋 使い方</h3>
                             <ul className="text-blue-800 space-y-2">
                 <li>• 選択肢をクリックして回答を選択してください</li>
                 <li>• 回答後、自動的に正誤判定とフィードバックが表示されます</li>
                 <li>• 解説が表示された後、次の問題に進むことができます</li>
                 <li>• 上部の進捗バーで全体の進捗を確認できます</li>
               </ul>
            </div>
          </div>

          {/* クイズ概要 */}
          <div className="max-w-4xl mx-auto mb-8">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">📚 クイズ内容</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <div className="text-2xl font-bold text-blue-600">{totalQuestions}</div>
                  <div className="text-sm text-gray-600">問題数</div>
                </div>
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <div className="text-2xl font-bold text-green-600">基礎</div>
                  <div className="text-sm text-gray-600">難易度</div>
                </div>
                <div className="text-center p-4 bg-gray-50 rounded-lg">
                  <div className="text-2xl font-bold text-purple-600">5分</div>
                  <div className="text-sm text-gray-600">予想時間</div>
                </div>
              </div>
              <div className="text-gray-600 mb-6">
                <p>HTML、CSS、JavaScriptの基礎知識に関する問題です。</p>
                <p>Web開発を学習中の方に最適なレベルとなっています。</p>
              </div>
            </div>
          </div>

          {/* 開始ボタン */}
          <div className="text-center">
            <button
              onClick={handleStartQuiz}
              className="px-8 py-4 bg-blue-600 text-white text-lg font-semibold rounded-lg hover:bg-blue-700 transition-colors shadow-lg"
            >
              🚀 クイズを開始する
            </button>
          </div>
        </div>
      </div>
    );
  }

  // クイズ実行中の画面
  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        {/* ヘッダー */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            HTML/CSS/JavaScript クイズ
          </h1>
          <p className="text-gray-600">
            Web開発の基礎知識をテストしてみましょう！
          </p>
        </div>

        {/* クイズ問題コンポーネント */}
        <QuizQuestion
          question={currentQuestion}
          currentQuestionNumber={currentQuestionIndex + 1}
          totalQuestions={totalQuestions}
          selectedAnswer={selectedAnswers[currentQuestion.id]}
          onAnswerSelect={handleAnswerSelect}
          onAnswerSubmit={handleAnswerSubmit}
          onNextQuestion={handleNextQuestion}
          onPreviousQuestion={handlePreviousQuestion}
          isFirstQuestion={currentQuestionIndex === 0}
          isLastQuestion={currentQuestionIndex === totalQuestions - 1}
          answeredQuestionsCount={answeredQuestionsCount}
          isAnswered={answeredQuestions.has(currentQuestion.id)}
        />
      </div>
    </div>
  );
};

export default QuizQuestionDemo; 