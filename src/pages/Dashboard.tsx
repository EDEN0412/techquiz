import { Book, Code, Database, Github as Git, Terminal, Cpu } from 'lucide-react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../components/ui/Card';
import { Button } from '../components/ui/Button';

const categories = [
  {
    id: 'html-css',
    title: 'HTML & CSS',
    description: 'Webの基礎とスタイリングを習得',
    icon: Code,
    color: 'text-orange-500',
    bgColor: 'bg-orange-50',
  },
  {
    id: 'python',
    title: 'Python',
    description: 'Python プログラミングの基礎から応用まで',
    icon: Terminal,
    color: 'text-blue-500',
    bgColor: 'bg-blue-50',
  },
  {
    id: 'git',
    title: 'Git',
    description: 'バージョン管理とチーム開発',
    icon: Git,
    color: 'text-gray-500',
    bgColor: 'bg-gray-50',
  },
  {
    id: 'linux',
    title: 'Linux コマンド',
    description: '基本的なターミナル操作',
    icon: Terminal,
    color: 'text-yellow-500',
    bgColor: 'bg-yellow-50',
  },
  {
    id: 'azure-ml',
    title: 'Azure ML',
    description: 'クラウドベースの機械学習',
    icon: Cpu,
    color: 'text-purple-500',
    bgColor: 'bg-purple-50',
  },
  {
    id: 'database',
    title: 'データベース',
    description: 'SQLとデータベース管理',
    icon: Database,
    color: 'text-green-500',
    bgColor: 'bg-green-50',
  },
];

const recentActivity = [
  {
    id: 1,
    category: 'Python',
    score: 85,
    date: '2024-03-10',
    difficulty: '中級',
  },
  {
    id: 2,
    category: 'Git',
    score: 92,
    date: '2024-03-09',
    difficulty: '初級',
  },
  {
    id: 3,
    category: 'HTML & CSS',
    score: 78,
    date: '2024-03-08',
    difficulty: '上級',
  },
];

export function Dashboard() {
  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">おかえりなさい！</h1>
          <p className="mt-1 text-lg text-gray-600">技術力を試してみましょう</p>
        </div>
        <div className="flex items-center space-x-4 rounded-lg bg-white p-4 shadow-sm">
          <div className="text-center">
            <p className="text-sm text-gray-500">完了したクイズ</p>
            <p className="text-2xl font-bold text-gray-900">12</p>
          </div>
          <div className="h-12 w-px bg-gray-200"></div>
          <div className="text-center">
            <p className="text-sm text-gray-500">平均スコア</p>
            <p className="text-2xl font-bold text-gray-900">85%</p>
          </div>
        </div>
      </div>

      {/* Categories Grid */}
      <div>
        <h2 className="mb-4 text-xl font-semibold text-gray-900">クイズカテゴリー</h2>
        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {categories.map((category) => {
            const Icon = category.icon;
            return (
              <Card key={category.id} interactive className="group cursor-pointer">
                <CardHeader>
                  <div className="mb-2 flex h-12 w-12 items-center justify-center rounded-lg group-hover:scale-110 transition-transform">
                    <Icon className={`h-8 w-8 ${category.color}`} />
                  </div>
                  <CardTitle>{category.title}</CardTitle>
                  <CardDescription>{category.description}</CardDescription>
                </CardHeader>
                <CardContent>
                  <Button className="w-full">クイズを開始</Button>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>

      {/* Recent Activity */}
      <div>
        <h2 className="mb-4 text-xl font-semibold text-gray-900">最近の活動</h2>
        <Card>
          <CardContent className="divide-y divide-gray-200">
            {recentActivity.map((activity) => (
              <div key={activity.id} className="flex items-center justify-between py-4 first:pt-0 last:pb-0">
                <div>
                  <p className="font-medium text-gray-900">{activity.category}</p>
                  <p className="text-sm text-gray-500">
                    {activity.difficulty} • {new Date(activity.date).toLocaleDateString('ja-JP')}
                  </p>
                </div>
                <div className="flex items-center space-x-4">
                  <div className="text-right">
                    <p className="text-lg font-semibold text-gray-900">{activity.score}%</p>
                    <p className="text-sm text-gray-500">スコア</p>
                  </div>
                  <Button variant="secondary" size="sm">
                    復習する
                  </Button>
                </div>
              </div>
            ))}
          </CardContent>
        </Card>
      </div>
    </div>
  );
}