# TechQuiz API実装予定

## 概要
フロントエンドの開発を優先するため、現在は各機能でモックデータを使用しています。
以下のAPIを後で実装する予定です。

## 実装が必要なAPI

### ✅ 既に実装済み（バックエンド）
- Django REST Framework の基本設定
- JWT認証システム
- 全モデルのCRUD操作
- シリアライザーとビューセット
- 基本的なAPIエンドポイント

### 🔧 実装中（フロントエンド）
- [x] カテゴリー選択機能（モックデータ使用中）
- [x] 難易度選択機能（モックデータ使用中）  
- [x] ダッシュボード統計表示（モックデータ使用中）
- [x] 最近の活動履歴（モックデータ使用中）

### 🚧 API接続の修正が必要

#### 1. カテゴリー管理API
**エンドポイント**: `GET /api/v1/quiz/categories/`

**現在の状況**: 
- バックエンドは実装済み
- フロントエンドはモックデータ使用中（`USE_MOCK_DATA = true`）

**修正タスク**:
- [ ] バックエンドサーバーの起動確認
- [ ] CORS設定の確認
- [ ] APIエンドポイントの動作テスト
- [ ] フロントエンドの`USE_MOCK_DATA`フラグをfalseに変更
- [ ] エラーハンドリングの改善

#### 2. 難易度管理API
**エンドポイント**: `GET /api/v1/quiz/difficulty-levels/`

**現在の状況**: 
- バックエンドは実装済み
- フロントエンドはモックデータ使用中

**修正タスク**:
- [ ] APIエンドポイントの動作テスト
- [ ] フロントエンドの`USE_MOCK_DATA`フラグをfalseに変更

#### 3. ユーザー統計API
**エンドポイント**: `GET /api/v1/quiz/user-stats-summary/`

**現在の状況**: 
- バックエンドは実装済み
- フロントエンドはモックデータ使用中

**修正タスク**:
- [ ] 認証が必要なAPIの動作確認
- [ ] JWTトークンの送信テスト
- [ ] フロントエンドの`USE_MOCK_DATA`フラグをfalseに変更

#### 4. 活動履歴API
**エンドポイント**: `GET /api/v1/quiz/recent-activities/`

**現在の状況**: 
- バックエンドは実装済み
- フロントエンドはモックデータ使用中

**修正タスク**:
- [ ] 認証が必要なAPIの動作確認
- [ ] データが空の場合の適切な処理
- [ ] フロントエンドの`USE_MOCK_DATA`フラグをfalseに変更

## API実装の優先順位

### Phase 1: 基本データ取得API
1. **カテゴリー取得API**の修正（認証不要）
2. **難易度取得API**の修正（認証不要）

### Phase 2: 認証が必要なAPI
3. **ユーザー統計API**の修正
4. **活動履歴API**の修正

### Phase 3: クイズ機能API
5. **クイズ取得API**の実装
6. **問題取得API**の実装
7. **回答送信API**の実装

## 開発手順

### 1. バックエンドの動作確認
```bash
cd backend
python manage.py runserver
```

### 2. APIエンドポイントのテスト
- `http://localhost:8000/api/v1/quiz/categories/`
- `http://localhost:8000/api/v1/quiz/difficulty-levels/`

### 3. フロントエンドの修正
各ファイルの`USE_MOCK_DATA`フラグを`false`に変更:
- `src/hooks/useCategories.ts`
- `src/pages/DifficultySelection.tsx`
- `src/hooks/useUserStats.ts`
- `src/hooks/useRecentActivities.ts`

### 4. CORS設定の確認
Django設定ファイルでCORSが適切に設定されているか確認

### 5. エラーハンドリングの改善
API接続エラー時の適切なフォールバック処理の実装

## 注意事項
- モックデータは実際のAPIのレスポンス形式と一致するように作成済み
- `USE_MOCK_DATA`フラグにより、開発中はモックデータ、本番ではAPIを使用可能
- API失敗時は自動的にモックデータにフォールバックする仕組みも実装済み

## Next Steps
1. バックエンドサーバーの起動とAPI動作確認
2. 各APIエンドポイントの個別テスト
3. フロントエンドでのAPI接続テスト
4. エラーケースの検証と改善
