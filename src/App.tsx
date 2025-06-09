import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Navbar } from './components/layout/Navbar';
import { Dashboard } from './pages/Dashboard';
import { SignUp } from './pages/SignUp';
import { Login } from './pages/Login';
import { DifficultySelection } from './pages/DifficultySelection';
import QuizPage from './pages/QuizPage';
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
            <Route path="/" element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/quiz" element={
              <ProtectedRoute>
                <div>クイズ画面</div>
              </ProtectedRoute>
            } />
            <Route path="/quiz/demo" element={<QuizQuestionDemo />} />
            <Route path="/quiz/:categoryId" element={
              <ProtectedRoute>
                <div>カテゴリー別クイズ画面</div>
              </ProtectedRoute>
            } />
            <Route path="/quiz/:categoryId/difficulty" element={
              <ProtectedRoute>
                <DifficultySelection />
              </ProtectedRoute>
            } />
            <Route path="/quiz/:categoryId/:difficultyId/start" element={
              <ProtectedRoute>
                <QuizPage />
              </ProtectedRoute>
            } />
            <Route path="/quiz/:categoryId/review" element={
              <ProtectedRoute>
                <QuizPage />
              </ProtectedRoute>
            } />
            <Route path="/results" element={
              <ProtectedRoute>
                <div>結果画面</div>
              </ProtectedRoute>
            } />
            <Route path="/profile" element={
              <ProtectedRoute>
                <div>プロフィール画面</div>
              </ProtectedRoute>
            } />
            <Route path="*" element={<div>404 - ページが見つかりません</div>} />
          </Routes>
        </main>
      </div>
    </Router>
    </AuthProvider>
  );
}

export default App;