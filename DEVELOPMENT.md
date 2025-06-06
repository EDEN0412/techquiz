# 開発環境管理ガイド

## 🚀 クイックスタート

### 開発環境の状態をチェック
```bash
npm run check:env
# または
./scripts/check-dev-env.sh
```

### 開発サーバーの起動（自動復旧機能付き）
```bash
npm run start:dev
# または
./dev.sh
```

## 🔧 Supabase管理コマンド

### 基本的な操作
```bash
# 状態確認
npm run supabase:status

# 手動起動
npm run supabase:start

# 手動停止
npm run supabase:stop

# 完全リセット（停止→起動）
npm run supabase:reset
```

## 🛡️ 自動復旧機能

### 新機能の説明
1. **起動時の自動チェック**: `dev.sh`実行時にSupabaseの状態を確認し、必要に応じて自動起動
2. **リアルタイム監視**: 30秒間隔でSupabaseの状態を監視し、停止を検出すると自動復旧
3. **リトライ機能**: 起動に失敗した場合、最大3回まで自動的に再試行

### 監視機能の動作
- 開発サーバー起動後、バックグラウンドで監視プロセスが動作
- Supabaseが予期せず停止した場合、コンソールに警告メッセージが表示
- 自動的に復旧処理が実行される

## 🔍 トラブルシューティング

### よくある問題と解決方法

#### 1. Supabaseが起動しない
```bash
# Docker状態を確認
docker info

# Dockerが停止している場合は起動
open -a Docker  # macOSの場合

# 完全リセットを試行
npm run supabase:reset
```

#### 2. 環境変数ファイルが不足
```bash
# 不足ファイルをコピー
cp .env.example .env.development
cp backend/.env.example backend/.env

# 適切な値を設定
```

#### 3. 依存関係の問題
```bash
# Node.js依存関係の再インストール
npm install

# Python依存関係の再インストール（Poetry使用時）
cd backend
poetry install
cd ..
```

## 📅 日常的な使用方法

### 開発開始時（推奨）
1. PCを起動したら
2. `npm run check:env` で環境を確認
3. `npm run start:dev` で開発サーバーを起動

### トラブルが発生した場合
1. `npm run supabase:status` でSupabaseの状態確認
2. 問題があれば `npm run supabase:reset` で完全リセット
3. それでも解決しない場合は `npm run check:env` でシステム全体をチェック

## ⚙️ 高度な設定

### 監視間隔の変更
`dev.sh`の以下の行を編集:
```bash
sleep 30  # 30秒ごとにチェック → 任意の秒数に変更
```

### 自動復旧の無効化
`dev.sh`実行時に監視機能をスキップしたい場合:
```bash
# 監視機能を一時的に無効化する場合は、dev.shを直接編集
# start_supabase_monitor の呼び出しをコメントアウト
```

## 🎯 ベストプラクティス

1. **毎日の開発開始時**: `npm run check:env`を実行
2. **PCを再起動した後**: 必ずSupabaseの状態を確認
3. **長時間の離席後**: 開発環境が正常に動作していることを確認
4. **エラーが発生した場合**: まず`supabase:status`で状態確認

これらの機能により、Supabaseの予期しない停止による開発の中断を最小限に抑えることができます。 