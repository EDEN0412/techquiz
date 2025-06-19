import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../lib/contexts/AuthContext';
import { Button } from '../components/ui/Button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { User, Mail, Calendar, Edit2, Save, X } from 'lucide-react';
import { userService } from '../lib/api/services/user.service';

export function Profile() {
  const { user, updateUser } = useAuth();
  const navigate = useNavigate();
  const [isEditing, setIsEditing] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  
  // 編集用のフォームデータ
  const [formData, setFormData] = useState({
    username: user?.username || '',
    email: user?.email || ''
  });

  // ユーザー情報が変更されたらフォームデータを更新
  useEffect(() => {
    if (user) {
      setFormData({
        username: user.username || '',
        email: user.email || ''
      });
    }
  }, [user]);

  // ユーザーが存在しない場合はログインページへリダイレクト
  if (!user) {
    navigate('/login');
    return null;
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
    setError(null);
    setSuccessMessage(null);
  };

  const handleEditClick = () => {
    setIsEditing(true);
    setError(null);
    setSuccessMessage(null);
  };

  const handleCancelEdit = () => {
    // 元のデータに戻す
    setFormData({
      username: user.username || '',
      email: user.email || ''
    });
    setIsEditing(false);
    setError(null);
    setSuccessMessage(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccessMessage(null);
    setLoading(true);

    try {
      // APIを呼び出してユーザー情報を更新
      const updatedUser = await userService.updateProfile(user.id, formData);
      
      // AuthContextのユーザー情報を更新
      updateUser(updatedUser);
      
      setIsEditing(false);
      setSuccessMessage('プロフィールを更新しました');
      
      // 3秒後に成功メッセージを消す
      setTimeout(() => {
        setSuccessMessage(null);
      }, 3000);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('プロフィールの更新に失敗しました');
      }
    } finally {
      setLoading(false);
    }
  };

  // 日付フォーマット関数
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('ja-JP', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  return (
    <div className="max-w-2xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">プロフィール</h1>
        <p className="mt-2 text-gray-600">アカウント情報の確認・編集ができます</p>
      </div>

      {/* 成功メッセージ */}
      {successMessage && (
        <div className="mb-4 rounded-md bg-green-50 p-4 text-sm text-green-700">
          {successMessage}
        </div>
      )}

      {/* エラーメッセージ */}
      {error && (
        <div className="mb-4 rounded-md bg-red-50 p-4 text-sm text-red-700">
          {error}
        </div>
      )}

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>基本情報</CardTitle>
              <CardDescription>ユーザー名とメールアドレスを管理できます</CardDescription>
            </div>
            {!isEditing && (
              <Button
                variant="secondary"
                size="sm"
                onClick={handleEditClick}
              >
                <Edit2 className="mr-2 h-4 w-4" />
                編集
              </Button>
            )}
          </div>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* ユーザー名 */}
            <div>
              <label className="flex items-center text-sm font-medium text-gray-700 mb-2">
                <User className="mr-2 h-4 w-4" />
                ユーザー名
              </label>
              {isEditing ? (
                <input
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleChange}
                  required
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
                />
              ) : (
                <p className="text-gray-900">{user.username}</p>
              )}
            </div>

            {/* メールアドレス */}
            <div>
              <label className="flex items-center text-sm font-medium text-gray-700 mb-2">
                <Mail className="mr-2 h-4 w-4" />
                メールアドレス
              </label>
              {isEditing ? (
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
                />
              ) : (
                <p className="text-gray-900">{user.email}</p>
              )}
            </div>

            {/* 登録日 */}
            <div>
              <label className="flex items-center text-sm font-medium text-gray-700 mb-2">
                <Calendar className="mr-2 h-4 w-4" />
                登録日
              </label>
              <p className="text-gray-900">{formatDate(user.date_joined)}</p>
            </div>

            {/* 編集モードのボタン */}
            {isEditing && (
              <div className="flex justify-end space-x-3 pt-4">
                <Button
                  type="button"
                  variant="secondary"
                  onClick={handleCancelEdit}
                  disabled={loading}
                >
                  <X className="mr-2 h-4 w-4" />
                  キャンセル
                </Button>
                <Button
                  type="submit"
                  disabled={loading}
                >
                  <Save className="mr-2 h-4 w-4" />
                  {loading ? '保存中...' : '保存'}
                </Button>
              </div>
            )}
          </form>
        </CardContent>
      </Card>

      {/* 今後の機能追加予定 */}
      <Card className="mt-6">
        <CardHeader>
          <CardTitle>その他の設定</CardTitle>
          <CardDescription>今後追加予定の機能</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-3 text-sm text-gray-600">
            <div className="flex items-center">
              <span className="mr-2">🔐</span>
              <span>パスワード変更（実装予定）</span>
            </div>
            <div className="flex items-center">
              <span className="mr-2">🎨</span>
              <span>テーマ設定（実装予定）</span>
            </div>
            <div className="flex items-center">
              <span className="mr-2">🗑️</span>
              <span>アカウント削除（実装予定）</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
} 