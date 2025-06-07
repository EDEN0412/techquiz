# 🛠️ トラブルシューティングガイド

## 🔥 緊急時の対処法

### Supabaseサービスが突然停止した場合

**症状:** `connection refused` エラー、port 54321 への接続失敗

**即座にできる対処法:**
```bash
# 1. 現状確認
npm run supabase:status

# 2. 自動復旧
npm run supabase:reset

# 3. 完全リセット（上記で解決しない場合）
npm run reset:env
```

### 認証エラー（401 Unauthorized）が発生した場合

**症状:** ログイン時に401エラー、APIアクセス拒否

**対処法:**
```bash
# 1. サーバーの再起動
Ctrl+C でdev.shを停止
./dev.sh で再起動

# 2. 環境チェック
npm run check:health

# 3. 完全リセット（必要に応じて）
npm run reset:env
```

---

## 📋 定期チェック

### 開発開始前（推奨）

```bash
# プリフライトチェック実行
npm run check:preflight
```

### 開発中に問題を感じた時

```bash
# ヘルスチェック実行
npm run check:health
```

---

## 🔍 問題診断フロー

### Step 1: 基本状況確認

```bash
# 全体状況の確認
npm run check:health

# Supabase状態の確認
npm run supabase:status

# プロセス確認
lsof -i :5173  # フロントエンド
lsof -i :8000  # バックエンド
lsof -i :54321 # Supabase
```

### Step 2: サービス別トラブルシューティング

#### 🌐 フロントエンド（Vite）の問題

**症状:**
- `http://localhost:5173` にアクセスできない
- ビルドエラー
- 画面が真っ白

**対処法:**
```bash
# キャッシュクリア
rm -rf node_modules/.vite
rm -rf .vite

# 依存関係再インストール
npm ci

# 開発サーバー再起動
./dev.sh
```

#### 🐍 バックエンド（Django）の問題

**症状:**
- `http://localhost:8000` にアクセスできない
- 500 Internal Server Error
- マイグレーションエラー

**対処法:**
```bash
cd backend

# 環境変数確認
cat .env

# データベース接続確認
python manage.py dbshell

# マイグレーション状態確認
python manage.py showmigrations

# マイグレーション実行
python manage.py migrate

cd ..
```

#### 🗄️ Supabase の問題

**症状:**
- `connection refused` エラー
- Supabase Studio にアクセスできない
- データベース接続エラー

**対処法:**
```bash
# Supabase完全リセット
npx supabase stop
docker system prune -f
npx supabase start

# 設定確認
cat supabase/config.toml

# 接続テスト
psql postgresql://postgres:postgres@localhost:54322/postgres -c "SELECT 1;"
```

---

## 🚨 よくある問題と解決法

### 1. ポート衝突

**エラー:** `EADDRINUSE: address already in use`

**解決法:**
```bash
# 使用中のプロセスを確認・停止
lsof -i :<PORT_NUMBER>
kill -9 <PID>

# または完全リセット
npm run reset:env
```

### 2. 環境変数の問題

**症状:** 設定値が反映されない、接続エラー

**解決法:**
```bash
# 環境変数ファイルの確認
ls -la .env*
ls -la backend/.env*

# ファイルの中身確認
cat .env.development
cat backend/.env

# サンプルファイルからコピー（必要に応じて）
cp .env.example .env.development
cp backend/.env.example backend/.env
```

### 3. 依存関係の問題

**症状:** パッケージが見つからない、バージョン衝突

**解決法:**
```bash
# フロントエンド
rm -rf node_modules package-lock.json
npm ci

# バックエンド（Poetryを使用している場合）
cd backend
poetry install

# または pip の場合
pip install -r requirements.txt
cd ..
```

### 4. データベーススキーマの不整合

**症状:** マイグレーション失敗、テーブルが見つからない

**解決法:**
```bash
cd backend

# マイグレーション状態確認
python manage.py showmigrations

# マイグレーションリセット
python manage.py migrate --fake-initial

# Supabase同期
python manage.py sync_supabase

cd ..
```

---

## 🔄 完全リセット手順

**注意:** この操作により全ての開発データが失われます

```bash
# 1. 確認
npm run check:health

# 2. 完全リセット実行
npm run reset:env

# 3. 環境変数設定（必要に応じて）
cp .env.example .env.development
cp backend/.env.example backend/.env
# ファイルを編集して適切な値を設定

# 4. 開発環境起動
./dev.sh

# 5. 動作確認
npm run check:health
```

---

## 📞 サポート情報

### ログファイルの場所

- **Django:** `backend/debug.log`
- **Vite:** ターミナル出力
- **Supabase:** Docker logs

### 有用なコマンド

```bash
# Docker関連の情報
docker ps -a
docker volume ls
docker system df

# システムリソース確認
df -h      # ディスク使用量
free -h    # メモリ使用量（Linux）
top        # プロセス確認
```

### 開発環境の復旧手順（緊急時）

1. `npm run reset:env` - 完全リセット
2. `.env` ファイルの再設定
3. `./dev.sh` - 開発環境起動
4. `npm run check:health` - 動作確認

---

## 🔐 セキュリティ注意事項

- `.env` ファイルを絶対にgitにコミットしないでください
- APIキーや機密情報は適切に管理してください
- 開発環境のパスワードを本番環境で使用しないでください

---

## 📝 問題レポート

問題が解決しない場合は、以下の情報を含めて報告してください：

1. **エラーメッセージ** （完全なスタックトレース）
2. **再現手順**
3. **環境情報** （OS、Node.js、Python、Dockerのバージョン）
4. **ログファイル** （該当部分の抜粋）
5. **試行した解決策**

**情報収集コマンド:**
```bash
# システム情報
node --version
python --version
docker --version
npx supabase --version

# ヘルスチェック結果
npm run check:health > health-report.txt

# 環境変数（機密情報を除く）
env | grep -E "(NODE_|PYTHON_|DJANGO_)" 
``` 