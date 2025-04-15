#!/bin/bash

# カラー設定
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ロゴ表示
echo -e "${CYAN}"
echo "████████╗███████╗ ██████╗██╗  ██╗ ██████╗ ██╗   ██╗██╗███████╗"
echo "╚══██╔══╝██╔════╝██╔════╝██║  ██║██╔═══██╗██║   ██║██║╚══███╔╝"
echo "   ██║   █████╗  ██║     ███████║██║   ██║██║   ██║██║  ███╔╝ "
echo "   ██║   ██╔══╝  ██║     ██╔══██║██║▄▄ ██║██║   ██║██║ ███╔╝  "
echo "   ██║   ███████╗╚██████╗██║  ██║╚██████╔╝╚██████╔╝██║███████╗"
echo "   ╚═╝   ╚══════╝ ╚═════╝╚═╝  ╚═╝ ╚══▀▀═╝  ╚═════╝ ╚═╝╚══════╝"
echo -e "${NC}"
echo -e "${YELLOW}開発サーバー起動スクリプト${NC}"
echo -e "${BLUE}----------------------------------------${NC}"

# 環境変数ファイルの存在確認
if [ ! -f ".env.development" ]; then
  echo -e "${RED}エラー: .env.development ファイルが見つかりません${NC}"
  echo -e "${YELLOW}.env.example をコピーして .env.development を作成してください${NC}"
  exit 1
fi

if [ ! -f "backend/.env" ]; then
  echo -e "${RED}エラー: backend/.env ファイルが見つかりません${NC}"
  echo -e "${YELLOW}backend/.env.example をコピーして backend/.env を作成してください${NC}"
  exit 1
fi

# 必要なツールの確認
if ! command -v node &> /dev/null; then
  echo -e "${RED}エラー: Node.js がインストールされていません${NC}"
  echo -e "${YELLOW}Node.js をインストールしてから再度実行してください${NC}"
  exit 1
fi

if ! command -v npx &> /dev/null; then
  echo -e "${RED}エラー: npx がインストールされていません${NC}"
  echo -e "${YELLOW}Node.js を最新版にアップデートするか、npm install -g npx を実行してください${NC}"
  exit 1
fi

# Supabase CLI の確認
if ! npx supabase --version &> /dev/null; then
  echo -e "${YELLOW}警告: Supabase CLI が見つかりません。インストールします...${NC}"
  npm install -g supabase
fi

# Docker が実行中か確認
if ! command -v docker &> /dev/null; then
  echo -e "${RED}エラー: Docker がインストールされていません${NC}"
  exit 1
fi

if ! docker info &> /dev/null; then
  echo -e "${RED}エラー: Docker デーモンが実行されていません${NC}"
  echo -e "${YELLOW}Docker を起動してから再度実行してください${NC}"
  exit 1
fi

# Poetry の確認
HAS_POETRY=true
if ! command -v poetry &> /dev/null; then
  echo -e "${YELLOW}警告: Poetry がインストールされていません。通常の Python を使用します${NC}"
  HAS_POETRY=false
fi

# 仮想環境のチェック
echo -e "${BLUE}環境のセットアップ...${NC}"

# Dockerモードでの起動
if [ "$1" == "--docker" ]; then
  echo -e "${GREEN}Dockerモードで開発環境を起動します...${NC}"
  docker-compose up
  exit 0
fi

# ローカルモードでの起動
echo -e "${GREEN}ローカルモードで開発環境を起動します...${NC}"

# Supabase の起動
echo -e "${YELLOW}Supabase を起動しています...${NC}"
npx supabase start &
SUPABASE_PID=$!

# バックグラウンドでバックエンドサーバーを起動
echo -e "${YELLOW}バックエンドサーバーを起動中...${NC}"
cd backend || exit
if [ "$HAS_POETRY" = true ]; then
  poetry run python manage.py runserver 0.0.0.0:8000 &
else
  python manage.py runserver 0.0.0.0:8000 &
fi
BACKEND_PID=$!
cd ..

# フロントエンドサーバーを起動
echo -e "${YELLOW}フロントエンドサーバーを起動中...${NC}"
npm run dev &
FRONTEND_PID=$!

# 終了処理の関数
cleanup() {
  echo -e "\n${YELLOW}開発サーバーを停止しています...${NC}"
  
  # プロセスを終了
  kill $FRONTEND_PID 2>/dev/null
  kill $BACKEND_PID 2>/dev/null
  
  # Supabaseを停止
  npx supabase stop
  
  echo -e "${GREEN}開発環境を正常に停止しました${NC}"
  exit 0
}

# Ctrl+C で終了時に cleanup を実行
trap cleanup SIGINT SIGTERM

echo -e "${GREEN}開発環境が起動しました！${NC}"
echo -e "${CYAN}フロントエンド: ${NC}http://localhost:5173"
echo -e "${CYAN}バックエンド: ${NC}http://localhost:8000"
echo -e "${CYAN}Supabase Studio: ${NC}http://localhost:54322"
echo -e "${BLUE}----------------------------------------${NC}"
echo -e "${YELLOW}終了するには Ctrl+C を押してください${NC}"

# すべてのバックグラウンドプロセスが終了するまで待機
wait 