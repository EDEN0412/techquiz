import React from 'react';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { QuizResultResponse } from '../lib/api/types';

export function QuizResultDetail() {
  const navigate = useNavigate();
  const location = useLocation();
  const { id } = useParams<{ id: string }>();

  // locationのstateからクイズ結果データを取得
  const quizResult = location.state?.quizResult as QuizResultResponse;

  // データが取得できない場合の処理
  if (!quizResult) {
    return (
      <div className="max-w-4xl mx-auto space-y-8">
        <Card>
          <CardContent className="py-8 text-center">
            <p className="text-red-500 mb-4">クイズ結果データが見つかりません</p>
            <Button onClick={() => navigate('/completed-quizzes')}>
              完了したクイズ一覧に戻る
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  // スコアに基づく色を決定
  const getScoreColor = (percentage: number): string => {
    if (percentage >= 80) return 'text-green-600';
    if (percentage >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  // 復習機能
  const handleReviewQuiz = () => {
    navigate(`/quiz/review/${quizResult.quiz}`, {
      state: { fromQuizDetail: true }
    });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* ヘッダー */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">クイズ結果詳細</h1>
          <p className="mt-1 text-lg text-gray-600">
            {quizResult.quiz_title}の結果詳細
          </p>
        </div>
        <div className="flex space-x-4">
          <Button 
            variant="secondary" 
            onClick={() => navigate('/completed-quizzes')}
          >
            一覧に戻る
          </Button>
          <Button 
            onClick={handleReviewQuiz}
          >
            復習する
          </Button>
        </div>
      </div>

      {/* メイン結果カード */}
      <Card className="border-2">
        <CardHeader className="pb-4">
          <div>
            <CardTitle className="text-2xl">{quizResult.quiz_title}</CardTitle>
            <CardDescription className="text-lg mt-2">
              {quizResult.category_name} • {quizResult.difficulty_name}
            </CardDescription>
          </div>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* スコア表示 */}
          <div className="text-center bg-gray-50 rounded-lg p-6">
            <div className={`text-6xl font-bold ${getScoreColor(quizResult.percentage)} mb-2`}>
              {Math.round(quizResult.percentage)}%
            </div>
            <p className="text-xl text-gray-600">
              {quizResult.score}点 / {quizResult.total_possible}点
            </p>
          </div>

          {/* 詳細情報 */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">基本情報</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">カテゴリー:</span>
                  <span className="font-medium">{quizResult.category_name}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">難易度:</span>
                  <span className="font-medium">{quizResult.difficulty_name}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">完了日時:</span>
                  <span className="font-medium">
                    {new Date(quizResult.completed_at).toLocaleString('ja-JP')}
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">所要時間:</span>
                  <span className="font-medium">
                    {Math.floor(quizResult.time_taken / 60)}分{quizResult.time_taken % 60}秒
                  </span>
                </div>
              </div>
            </div>

            <div className="space-y-4">
              <h3 className="text-lg font-semibold text-gray-900">結果分析</h3>
              <div className="space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">正答率:</span>
                  <span className={`font-medium ${getScoreColor(quizResult.percentage)}`}>
                    {Math.round(quizResult.percentage)}%
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">平均所要時間:</span>
                  <span className="font-medium">
                    {Math.round(quizResult.time_taken / (quizResult.total_possible || 1))}秒/問
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* パフォーマンス評価 */}
          <div className="bg-blue-50 rounded-lg p-4">
            <h3 className="text-lg font-semibold text-blue-900 mb-2">パフォーマンス評価</h3>
            <div className="text-sm text-blue-800">
              {quizResult.percentage >= 90 ? (
                <p>🎉 素晴らしい結果です！完璧に理解されています。</p>
              ) : quizResult.percentage >= 80 ? (
                <p>✨ とても良い成績です！少しの復習でさらに向上できるでしょう。</p>
              ) : quizResult.percentage >= 70 ? (
                <p>👍 良い成績です！いくつかの分野を復習することをお勧めします。</p>
              ) : quizResult.percentage >= 60 ? (
                <p>📚 基本は身についています。復習して理解を深めましょう。</p>
              ) : (
                <p>💪 まだ理解が不十分な部分があります。基礎から復習することをお勧めします。</p>
              )}
            </div>
          </div>

          {/* アクションボタン */}
          <div className="flex justify-center space-x-4 pt-4">
            <Button 
              variant="secondary" 
              onClick={() => navigate('/completed-quizzes')}
            >
              完了したクイズ一覧
            </Button>
            <Button 
              onClick={handleReviewQuiz}
            >
              このクイズを復習する
            </Button>
            <Button 
              variant="outline" 
              onClick={() => navigate('/')}
            >
              ダッシュボード
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
} 