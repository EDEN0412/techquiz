import { Link } from 'react-router-dom';
import { Brain, User } from 'lucide-react';
import { Button } from '../ui/Button';

export function Navbar() {
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
            <Button variant="secondary" size="sm" asChild>
              <Link to="/profile">
                <User className="mr-2 h-4 w-4" />
                プロフィール
              </Link>
            </Button>
          </div>
        </div>
      </div>
    </nav>
  );
}