import React from 'react';
import { QuizQuestion as QuizQuestionType } from '../../lib/api/types';

interface QuizResultData {
  totalQuestions: number;
  correctAnswers: number;
  score: number;
  timeSpent?: number;
  questions: QuizQuestionResult[];
}

interface QuizQuestionResult {
  question: QuizQuestionType;
  selectedAnswerId: number;
  isCorrect: boolean;
  timeSpent?: number;
}

interface QuizResultProps {
  resultData: QuizResultData;
  onRestartQuiz: () => void;
  onGoHome: () => void;
  quizTitle?: string;
}

const QuizResult: React.FC<QuizResultProps> = ({
  resultData,
  onRestartQuiz,
  onGoHome,
  quizTitle = "クイズ"
}) => {
  const { totalQuestions, correctAnswers, score, questions } = resultData;
  const percentage = Math.round((correctAnswers / totalQuestions) * 100);

  // スコアに基づくメッセージとアイコン
  const getScoreMessage = () => {
    if (percentage >= 90) {
      return {
        icon: "🏆",
        title: "素晴らしい！",
        message: "完璧に近い成績です！",
        color: "text-yellow-600",
        bgColor: "bg-yellow-50",
        borderColor: "border-yellow-300"
      };
    } else if (percentage >= 70) {
      return {
        icon: "🎉",
        title: "よくできました！",
        message: "良い成績です！",
        color: "text-green-600",
        bgColor: "bg-green-50",
        borderColor: "border-green-300"
      };
    } else if (percentage >= 50) {
      return {
        icon: "👍",
        title: "合格です！",
        message: "もう少し頑張りましょう！",
        color: "text-blue-600",
        bgColor: "bg-blue-50",
        borderColor: "border-blue-300"
      };
    } else {
      return {
        icon: "💪",
        title: "惜しい！",
        message: "復習してもう一度挑戦しましょう！",
        color: "text-orange-600",
        bgColor: "bg-orange-50",
        borderColor: "border-orange-300"
      };
    }
  };

  const scoreMessage = getScoreMessage();

  return (
    <div className="min-h-screen bg-gray-100 py-8">
      <div className="container mx-auto px-4">
        {/* ヘッダー */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            {quizTitle} 結果
          </h1>
          <p className="text-gray-600">
            お疲れさまでした！結果をご確認ください。
          </p>
        </div>

        {/* スコア表示 */}
        <div className="max-w-4xl mx-auto mb-8">
          <div className={`${scoreMessage.bgColor} border ${scoreMessage.borderColor} rounded-lg p-8 text-center`}>
            <div className="text-6xl mb-4">{scoreMessage.icon}</div>
            <h2 className={`text-2xl font-bold ${scoreMessage.color} mb-2`}>
              {scoreMessage.title}
            </h2>
            <p className={`${scoreMessage.color} mb-6`}>
              {scoreMessage.message}
            </p>
            
            {/* スコア詳細 */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-white rounded-lg p-4 shadow-sm">
                <div className="text-3xl font-bold text-blue-600">{correctAnswers}</div>
                <div className="text-sm text-gray-600">正解数</div>
              </div>
              <div className="bg-white rounded-lg p-4 shadow-sm">
                <div className="text-3xl font-bold text-purple-600">{totalQuestions}</div>
                <div className="text-sm text-gray-600">問題数</div>
              </div>
              <div className="bg-white rounded-lg p-4 shadow-sm">
                <div className="text-3xl font-bold text-green-600">{percentage}%</div>
                <div className="text-sm text-gray-600">正答率</div>
              </div>
            </div>

            {/* 進捗バー */}
            <div className="w-full bg-gray-200 rounded-full h-4 mb-4">
              <div 
                className="bg-gradient-to-r from-green-400 to-green-600 h-4 rounded-full transition-all duration-1000 ease-out"
                style={{ width: `${percentage}%` }}
              ></div>
            </div>
            <p className="text-sm text-gray-600">
              {correctAnswers} / {totalQuestions} 問正解
            </p>
          </div>
        </div>

        {/* 問題別結果一覧 */}
        <div className="max-w-4xl mx-auto mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-xl font-bold text-gray-900 mb-6 flex items-center">
              📋 問題別結果
            </h3>
            
            <div className="space-y-4">
              {questions.map((questionResult, index) => {
                const correctAnswer = questionResult.question.answers.find(a => a.is_correct);
                const selectedAnswer = questionResult.question.answers.find(a => a.id === questionResult.selectedAnswerId);
                
                return (
                  <div key={questionResult.question.id} className="border rounded-lg p-4">
                    <div className="flex items-start justify-between mb-3">
                      <div className="flex items-center space-x-3">
                        <span className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold ${
                          questionResult.isCorrect 
                            ? 'bg-green-100 text-green-800' 
                            : 'bg-red-100 text-red-800'
                        }`}>
                          {index + 1}
                        </span>
                        <span className="text-2xl">
                          {questionResult.isCorrect ? '✅' : '❌'}
                        </span>
                      </div>
                      <div className={`px-3 py-1 rounded-full text-sm font-medium ${
                        questionResult.isCorrect 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {questionResult.isCorrect ? '正解' : '不正解'}
                      </div>
                    </div>
                    
                    <div className="mb-3">
                      <h4 className="font-medium text-gray-900 mb-2">
                        問題 {index + 1}: {questionResult.question.question_text}
                      </h4>
                      
                      <div className="space-y-2 text-sm">
                        <div className="flex items-center space-x-2">
                          <span className="text-gray-600">あなたの回答:</span>
                          <span className={`font-medium ${
                            questionResult.isCorrect ? 'text-green-600' : 'text-red-600'
                          }`}>
                            {selectedAnswer?.answer_text}
                          </span>
                        </div>
                        
                        {!questionResult.isCorrect && (
                          <div className="flex items-center space-x-2">
                            <span className="text-gray-600">正解:</span>
                            <span className="font-medium text-green-600">
                              {correctAnswer?.answer_text}
                            </span>
                          </div>
                        )}
                      </div>
                    </div>
                    
                    {questionResult.question.explanation && (
                      <div className="bg-blue-50 border-l-4 border-blue-400 p-3 mt-3">
                        <p className="text-sm text-blue-800">
                          <strong>解説:</strong> {questionResult.question.explanation}
                        </p>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>

        {/* アクションボタン */}
        <div className="max-w-4xl mx-auto text-center">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-6">
              次は何をしますか？
            </h3>
            
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <button
                onClick={onRestartQuiz}
                className="px-8 py-3 bg-blue-600 text-white font-medium rounded-lg hover:bg-blue-700 transition-colors shadow-lg flex items-center justify-center space-x-2"
              >
                <span>🔄</span>
                <span>もう一度挑戦</span>
              </button>
              
              <button
                onClick={onGoHome}
                className="px-8 py-3 bg-gray-200 text-gray-700 font-medium rounded-lg hover:bg-gray-300 transition-colors flex items-center justify-center space-x-2"
              >
                <span>🏠</span>
                <span>ホームに戻る</span>
              </button>
            </div>
            
            <div className="mt-6 text-sm text-gray-500">
              <p>🎯 さらに学習を進めて、より高いスコアを目指しましょう！</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default QuizResult; 