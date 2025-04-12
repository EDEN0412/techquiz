アプリケーション名	
アプリケーション概要	このアプリケーションでできることを記載。
URL	デプロイ済みのURLを記載。デプロイが済んでいない場合は、デプロイが完了次第記載すること。
テスト用アカウント	ログイン機能等を実装した場合は、ログインに必要な情報を記載。またBasic認証等を設けている場合は、そのID/Passも記載すること。
利用方法	このアプリケーションの利用方法を記載。説明が長い場合は、箇条書きでリスト化すること。
アプリケーションを作成した背景	このアプリケーションを通じて、どのような人の、どのような課題を解決しようとしているのかを記載。
実装した機能についての画像やGIFおよびその説明※	実装した機能について、それぞれどのような特徴があるのかを列挙する形で記載。画像はGyazoで、GIFはGyazoGIFで撮影すること。
実装予定の機能	洗い出した要件の中から、今後実装予定の機能がある場合は、その機能を記載。
データベース設計	ER図を添付。
画面遷移図	画面遷移図を添付。
開発環境	使用した言語・サービスを記載。
ローカルでの動作方法	git cloneしてから、ローカルで動作をさせるまでに必要なコマンドを記載。
工夫したポイント	制作背景・使用技術・開発方法・タスク管理など、企業へＰＲしたい事柄を記載。
改善点	より改善するとしたらどこか、それはどのようにしてやるのか。
制作時間	アプリケーションを制作するのにかけた時間。

# TechQuiz

技術スキル向上のためのクイズアプリケーション

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
