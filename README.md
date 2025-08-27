
# TechQuiz

技術スキル向上のためのクイズアプリケーション


# URL

resplendent-celebration-production.up.railway.app

## 開発環境のセットアップ

### 前提条件
- Node.js v18以上
- Python 3.9以上
- Docker & Docker Compose（ローカルSupabase環境用）

### 環境変数の設定

1. 開発環境用の`.env.development`を設定する:
```bash
# リポジトリのルートディレクトリにコピーして使用
cp .env.example .env.development
```

2. 必要な環境変数を設定:
   - Supabase接続情報
   - データベース接続情報
   - Djangoの設定値

### フロントエンド（React + TypeScript）

```bash
# 依存関係のインストール
npm install

# 開発サーバーの起動
npm run dev
```

### バックエンド（Django）

```bash
# 仮想環境の作成と有効化
python -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate

# 依存関係のインストール
cd backend
pip install -r requirements.txt

# 開発サーバーの起動
python manage.py runserver
```

### ローカルSupabase環境

```bash
# Supabase CLIがインストールされていることを確認
supabase --version

# ローカルSupabase環境の起動
supabase start

# ブラウザでStudioにアクセス
open http://localhost:54323
```

### データベースのフルリセット（ワンコマンド）

開発中にスキーマを壊してしまった場合や、クリーンな状態からやり直したい場合は **1 行だけ** で再構築できます。

```bash
# ルートディレクトリで実行
npm run db:reset
```

処理内容:
1. ローカル Supabase を再起動し、**スキーマのみ** をリセット
2. Django マイグレーションをすべて適用（`backend/manage.py migrate`）
3. `supabase/seed.sql` を流し込み、カテゴリ・難易度・クイズ問題などの初期データを投入

10〜15 分ほどで **API・フロントエンドとも動く状態** になります。

# マイグレーション関連ファイル
- [DBマイグレーション管理手順書](docs/db_migration_guidelines.md)
