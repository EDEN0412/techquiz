import { Link } from 'react-router-dom';
import { Brain, User, LogIn, Home } from 'lucide-react';
import { Button } from '../ui/Button';
import { useAuth } from '../../lib/contexts/AuthContext';

export function Navbar() {
  const { isAuthenticated, logout } = useAuth();

  return (
    <nav className="border-b border-gray-200 bg-white">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <Brain className="h-8 w-8 text-blue-500" />
              <span className="text-xl font-bold text-gray-900">TechQuiz</span>
            </Link>
          </div>
          <div className="flex items-center space-x-4">
            {isAuthenticated ? (
              <>
                <Link to="/">
                  <Button variant="outline" size="sm">
                    <Home className="mr-2 h-4 w-4" />
                    ダッシュボード
                  </Button>
                </Link>
                <Link to="/profile">
                  <Button variant="outline" size="sm">
                    <User className="mr-2 h-4 w-4" />
                    プロフィール
                  </Button>
                </Link>
                <Button onClick={logout} variant="secondary" size="sm">
                  ログアウト
                </Button>
              </>
            ) : (
              <>
                <Link to="/login">
                  <Button variant="outline" size="sm">
                    <LogIn className="mr-2 h-4 w-4" />
                    ログイン
                  </Button>
                </Link>
                <Link to="/signup">
                  <Button variant="primary" size="sm">
                    サインアップ
                  </Button>
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}