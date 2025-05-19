import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { register, RegisterData } from '../lib/api/services/authService';
import { useAuth } from '../lib/contexts/AuthContext';
import { Button } from '../components/ui/Button';

export function SignUp() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [formData, setFormData] = useState<Omit<RegisterData, 'first_name' | 'last_name'>>({
    username: '',
    password: '',
    password2: '',
    email: '',
  });
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);

    // パスワードの長さチェック
    if (formData.password.length < 4) {
      setError('パスワードは4文字以上で入力してください');
      setLoading(false);
      return;
    }

    // パスワード一致チェック
    if (formData.password !== formData.password2) {
      setError('パスワードが一致しません');
      setLoading(false);
      return;
    }

    try {
      // ユーザー登録（名前と姓はデフォルト値を設定）
      await register({
        ...formData,
        first_name: 'User',
        last_name: 'Account'
      });
      
      // 登録成功後、自動的にログイン
      const success = await login({
        username: formData.username,
        password: formData.password
      });
      
      if (success) {
        navigate('/');
      } else {
        setError('登録後のログインに失敗しました。ログインページからログインしてください。');
      }
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError('アカウント作成中に予期せぬエラーが発生しました');
      }
      console.error('Registration error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mx-auto max-w-md">
      <div className="rounded-lg border bg-white p-8 shadow-sm">
        <h1 className="text-center text-2xl font-bold text-gray-900 mb-6">アカウント作成</h1>
        
        {error && (
          <div className="mb-4 rounded-md bg-red-50 p-4 text-sm text-red-700">
            {error.split('\n').map((line, index) => (
              <div key={index}>{line}</div>
            ))}
          </div>
        )}
        
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="username" className="block text-sm font-medium text-gray-700">
              ユーザー名
            </label>
            <input
              id="username"
              name="username"
              type="text"
              required
              value={formData.username}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              メールアドレス
            </label>
            <input
              id="email"
              name="email"
              type="email"
              required
              value={formData.email}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              パスワード (4文字以上)
            </label>
            <input
              id="password"
              name="password"
              type="password"
              required
              minLength={4}
              value={formData.password}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label htmlFor="password2" className="block text-sm font-medium text-gray-700">
              パスワード（確認）
            </label>
            <input
              id="password2"
              name="password2"
              type="password"
              required
              minLength={4}
              value={formData.password2}
              onChange={handleChange}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-blue-500"
            />
          </div>
          
          <Button 
            type="submit" 
            className="w-full" 
            disabled={loading}
          >
            {loading ? '処理中...' : 'アカウント作成'}
          </Button>
        </form>
        
        <p className="mt-4 text-center text-sm text-gray-600">
          既にアカウントをお持ちですか？{' '}
          <Link to="/login" className="font-medium text-blue-600 hover:text-blue-500">
            ログイン
          </Link>
        </p>
      </div>
    </div>
  );
} 