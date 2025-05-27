import React, { useState, useEffect } from 'react';
import { QuizQuestion as QuizQuestionType, Answer } from '../../lib/api/types';

interface QuizQuestionProps {
  question: QuizQuestionType;
  currentQuestionNumber: number;
  totalQuestions: number;
  selectedAnswer?: number;
  onAnswerSelect: (answerId: number) => void;
  onAnswerSubmit: () => void;
  onNextQuestion: () => void;
  onPreviousQuestion: () => void;
  isFirstQuestion: boolean;
  isLastQuestion: boolean;
  answeredQuestionsCount?: number;
  isAnswered?: boolean;
}

const QuizQuestion: React.FC<QuizQuestionProps> = ({
  question,
  currentQuestionNumber,
  totalQuestions,
  selectedAnswer,
  onAnswerSelect,
  onAnswerSubmit,
  onNextQuestion,
  onPreviousQuestion,
  isFirstQuestion,
  isLastQuestion,
  answeredQuestionsCount = 0,
  isAnswered = false
}) => {
  const [isSubmitted, setIsSubmitted] = useState(false);

  // 問題が変わった時に状態をリセット
  useEffect(() => {
    setIsSubmitted(isAnswered);
  }, [question.id, isAnswered]);

  // 進捗の計算（回答済み問題数/全問題数）
  const progress = (answeredQuestionsCount / totalQuestions) * 100;

  // 正解を取得
  const getCorrectAnswer = () => {
    return question.answers.find(answer => answer.is_correct);
  };

  // 回答選択時の処理
  const handleAnswerSelect = (answerId: number) => {
    // 回答済みの問題では選択を無効にする
    if (isSubmitted) return;
    
    onAnswerSelect(answerId);
  };

  // 回答確定時の処理
  const handleAnswerSubmit = () => {
    if (!selectedAnswer || isSubmitted) return;
    
    onAnswerSubmit();
    setIsSubmitted(true);
  };

  // 選択肢のスタイル
  const getAnswerStyle = (answer: Answer) => {
    let style = "w-full p-4 text-left border-2 rounded-lg transition-all duration-300 ";
    
    if (!isSubmitted) {
      if (selectedAnswer === answer.id) {
        style += "border-blue-500 bg-blue-50 text-blue-900";
      } else {
        style += "border-gray-300 bg-white hover:border-blue-300 hover:bg-blue-50";
      }
    } else {
      if (answer.is_correct) {
        style += "border-green-500 bg-green-50 text-green-900";
      } else if (selectedAnswer === answer.id) {
        style += "border-red-500 bg-red-50 text-red-900";
      } else {
        style += "border-gray-300 bg-gray-50 text-gray-600";
      }
    }
    return style;
  };

  // フィードバックメッセージ
  const getFeedback = () => {
    if (!selectedAnswer || !isSubmitted) return null;
    const isCorrect = getCorrectAnswer()?.id === selectedAnswer;
    const correctAnswer = getCorrectAnswer();
    
    const messages = {
      correct: [
        "🎉 正解です！素晴らしい！",
        "✨ その通り！完璧です！",
        "🌟 正解！よく知っていますね！",
        "🎯 大正解！お見事です！"
      ],
      incorrect: [
        "❌ 残念！不正解です",
        "💭 惜しい！もう一度考えてみましょう",
        "🤔 違います。正解を確認しましょう",
        "📚 不正解です。学習のチャンスですね"
      ]
    };
    
    const randomMessage = isCorrect 
      ? messages.correct[Math.floor(Math.random() * messages.correct.length)]
      : messages.incorrect[Math.floor(Math.random() * messages.incorrect.length)];
    
    return {
      isCorrect,
      message: randomMessage,
      correctAnswerText: correctAnswer?.answer_text
    };
  };

  const feedback = getFeedback();

  return (
    <div className="max-w-4xl mx-auto p-6 bg-white rounded-lg shadow-lg">
      {/* 進捗バー */}
      <div className="mb-6">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700">
            問題 {currentQuestionNumber} / {totalQuestions}
          </span>
          <span className="text-sm text-gray-500">
            {Math.round(progress)}% 完了
          </span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div 
            className="bg-blue-600 h-3 rounded-full transition-all duration-500"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>

      {/* 問題文 */}
      <div className="mb-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-bold text-gray-900">
            問題 {currentQuestionNumber}
          </h2>

        </div>
        
        <div className="text-gray-800 text-lg leading-relaxed mb-4 p-4 bg-gray-50 rounded-lg">
          {question.question_text}
        </div>


      </div>

      {/* フィードバック */}
      {feedback && (
        <div className={`mb-6 p-4 rounded-lg border-l-4 ${
          feedback.isCorrect ? 'bg-green-50 border-green-400' : 'bg-red-50 border-red-400'
        }`}>
          <p className={`font-bold ${
            feedback.isCorrect ? 'text-green-800' : 'text-red-800'
          }`}>
            {feedback.message}
          </p>
                     {!feedback.isCorrect && (
             <p className="text-gray-600 mt-2 text-base">
               💡 正解: <span className="font-semibold text-gray-800">{feedback.correctAnswerText}</span>
             </p>
           )}
        </div>
      )}

      {/* 選択肢 */}
      <div className="mb-8">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">選択肢</h3>
        <div className="space-y-3">
          {question.answers
            .sort((a, b) => a.order - b.order)
            .map((answer, index) => (
              <button
                key={answer.id}
                onClick={() => handleAnswerSelect(answer.id)}
                className={getAnswerStyle(answer)}
                disabled={isSubmitted}
              >
                <div className="flex items-center">
                  <span className="w-8 h-8 bg-gray-200 rounded-full flex items-center justify-center text-sm font-medium mr-3">
                    {String.fromCharCode(65 + index)}
                  </span>
                  <span className="flex-1">{answer.answer_text}</span>
                  {isSubmitted && (
                    <span className="ml-2">
                      {answer.is_correct ? '✅' : selectedAnswer === answer.id ? '❌' : ''}
                    </span>
                  )}
                </div>
              </button>
            ))}
        </div>
      </div>

      {/* 解説 */}
      {isSubmitted && question.explanation && (
        <div className="mb-8 bg-blue-50 border-l-4 border-blue-400 p-4">
          <h4 className="text-lg font-semibold text-blue-900 mb-2">📖 解説</h4>
          <p className="text-blue-800">{question.explanation}</p>
        </div>
      )}

      {/* 回答ボタン */}
      {selectedAnswer && !isSubmitted && (
        <div className="mb-6 text-center">
          <button
            onClick={handleAnswerSubmit}
            className="px-8 py-3 bg-blue-600 text-white text-lg font-semibold rounded-lg hover:bg-blue-700 transition-colors shadow-lg"
          >
            📝 回答する
          </button>
        </div>
      )}

      {/* ナビゲーション */}
      <div className="flex justify-between items-center">
        <button
          onClick={onPreviousQuestion}
          disabled={isFirstQuestion}
          className={`px-6 py-2 rounded-lg font-medium ${
            isFirstQuestion
              ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
          }`}
        >
          ← 前の問題
        </button>

        <div className="flex items-center space-x-4">
          {selectedAnswer && !isSubmitted && (
            <span className="text-sm text-blue-600 font-medium flex items-center">
              <span className="w-2 h-2 bg-blue-500 rounded-full mr-2 animate-pulse"></span>
              回答を選択中...
            </span>
          )}
          {isSubmitted && (
            <span className="text-sm text-green-600 font-medium flex items-center">
              <span className="w-2 h-2 bg-green-500 rounded-full mr-2"></span>
              回答済み
            </span>
          )}
        </div>

        <button
          onClick={onNextQuestion}
          disabled={!isSubmitted}
          className={`px-6 py-2 rounded-lg font-medium ${
            !isSubmitted
              ? 'bg-gray-100 text-gray-400 cursor-not-allowed'
              : isLastQuestion
              ? 'bg-green-600 text-white hover:bg-green-700'
              : 'bg-blue-600 text-white hover:bg-blue-700'
          }`}
        >
          {isLastQuestion ? '結果を見る →' : '次の問題 →'}
        </button>
      </div>
    </div>
  );
};

export default QuizQuestion; 