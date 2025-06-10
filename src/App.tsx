import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Navbar } from './components/layout/Navbar';
import { Dashboard } from './pages/Dashboard';
import { SignUp } from './pages/SignUp';
import { Login } from './pages/Login';
import { DifficultySelection } from './pages/DifficultySelection';
import QuizPage from './pages/QuizPage';
import { CompletedQuizzes } from './pages/CompletedQuizzes';
import { QuizResultDetail } from './pages/QuizResultDetail';
import { AuthProvider } from './lib/contexts/AuthContext';
import QuizQuestionDemo from './components/quiz/QuizQuestionDemo';
import ProtectedRoute from './components/ProtectedRoute';


function App() {
  return (
    <AuthProvider>
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
          <Routes>
            {/* ホーム画面 - 認証不要 */}
            <Route path="/" element={<Dashboard />} />
            
            {/* 認証関連ページ */}
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<SignUp />} />
            
            {/* クイズ関連ページ - 認証不要 */}
            <Route path="/quiz" element={<div>クイズ画面</div>} />
            <Route path="/quiz/demo" element={<QuizQuestionDemo />} />
            <Route path="/quiz/:categoryId" element={<div>カテゴリー別クイズ画面</div>} />
            <Route path="/quiz/:categoryId/difficulty" element={<DifficultySelection />} />
            <Route path="/quiz/:categoryId/:difficultyId/start" element={<QuizPage />} />
            <Route path="/quiz/:categoryId/review" element={<QuizPage />} />
            <Route path="/quiz/review/:quizId" element={<QuizPage />} />
            <Route path="/results" element={<div>結果画面</div>} />
            
            {/* 認証が必要なページ */}
            <Route path="/profile" element={
              <ProtectedRoute>
                <div>プロフィール画面</div>
              </ProtectedRoute>
            } />
            
            {/* 完了したクイズ一覧ページ */}
            <Route path="/completed-quizzes" element={<CompletedQuizzes />} />
            
            {/* クイズ結果詳細ページ */}
            <Route path="/quiz-result/:id" element={<QuizResultDetail />} />
            
            {/* 404ページ */}
            <Route path="*" element={<div>404 - ページが見つかりません</div>} />
          </Routes>
        </main>
      </div>
    </Router>
    </AuthProvider>
  );
}

export default App;