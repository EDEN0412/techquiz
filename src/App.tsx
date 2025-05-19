import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Navbar } from './components/layout/Navbar';
import { Dashboard } from './pages/Dashboard';
import { SignUp } from './pages/SignUp';
import { AuthProvider } from './lib/contexts/AuthContext';

function App() {
  return (
    <AuthProvider>
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Navbar />
        <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/login" element={<div>ログイン画面</div>} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/quiz" element={<div>クイズ画面</div>} />
            <Route path="/quiz/:categoryId" element={<div>カテゴリー別クイズ画面</div>} />
            <Route path="/quiz/:categoryId/difficulty" element={<div>難易度選択画面</div>} />
            <Route path="/results" element={<div>結果画面</div>} />
            <Route path="/profile" element={<div>プロフィール画面</div>} />
            <Route path="*" element={<div>404 - ページが見つかりません</div>} />
          </Routes>
        </main>
      </div>
    </Router>
    </AuthProvider>
  );
}

export default App;