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
echo -e "${YELLOW}開発サーバー起動スクリプト（自動復旧機能付き）${NC}"
echo -e "${BLUE}----------------------------------------${NC}"

# Supabase状態チェック関数
check_supabase_status() {
  local status_output
  status_output=$(npx supabase status 2>/dev/null)
  
  if echo "$status_output" | grep -q "API URL: http://127.0.0.1:54321"; then
    return 0  # 正常動作中
  else
    return 1  # 停止中または問題あり
  fi
}

# Supabaseの自動起動・復旧関数
ensure_supabase_running() {
  echo -e "${BLUE}Supabaseの状態を確認中...${NC}"
  
  if check_supabase_status; then
    echo -e "${GREEN}✓ Supabaseは既に動作中です${NC}"
    return 0
  fi
  
  echo -e "${YELLOW}Supabaseが停止しています。起動中...${NC}"
  
  # 一度完全に停止してからクリーンに起動
  npx supabase stop >/dev/null 2>&1
  sleep 2
  
  # 起動試行
  local retry_count=0
  local max_retries=3
  
  while [ $retry_count -lt $max_retries ]; do
    echo -e "${YELLOW}Supabase起動試行 ($((retry_count + 1))/$max_retries)...${NC}"
    
    if npx supabase start; then
      sleep 5  # 起動完了を待機
      
      if check_supabase_status; then
        echo -e "${GREEN}✓ Supabaseが正常に起動しました${NC}"
        return 0
      fi
    fi
    
    retry_count=$((retry_count + 1))
    if [ $retry_count -lt $max_retries ]; then
      echo -e "${YELLOW}再試行します...${NC}"
      sleep 3
    fi
  done
  
  echo -e "${RED}エラー: Supabaseの起動に失敗しました${NC}"
  exit 1
}

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

# Supabaseの状態確認と自動起動
ensure_supabase_running

# 定期的なSupabase監視機能
start_supabase_monitor() {
  while true; do
    sleep 30  # 30秒ごとにチェック
    if ! check_supabase_status; then
      echo -e "${YELLOW}⚠️  Supabaseが停止しました。自動復旧中...${NC}"
      ensure_supabase_running
    fi
  done &
  MONITOR_PID=$!
}

# 監視開始
echo -e "${BLUE}Supabase監視機能を開始しています...${NC}"
start_supabase_monitor

# バックグラウンドでバックエンドサーバーを起動
echo -e "${YELLOW}バックエンドサーバーを起動中...${NC}"
cd backend || exit
if [ "$HAS_POETRY" = true ]; then
  DJANGO_ENV=development poetry run python manage.py runserver 0.0.0.0:8000 &
else
  DJANGO_ENV=development python manage.py runserver 0.0.0.0:8000 &
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
  
  # 監視プロセスを終了
  if [ ! -z "$MONITOR_PID" ]; then
    kill $MONITOR_PID 2>/dev/null
  fi
  
  # プロセスを終了
  kill $FRONTEND_PID 2>/dev/null
  kill $BACKEND_PID 2>/dev/null
  
  # Supabaseを停止
  echo -e "${YELLOW}Supabaseを停止中...${NC}"
  npx supabase stop
  
  echo -e "${GREEN}開発環境を正常に停止しました${NC}"
  exit 0
}

# Ctrl+C で終了時に cleanup を実行
trap cleanup SIGINT SIGTERM

echo -e "${GREEN}開発環境が起動しました！${NC}"
echo -e "${GREEN}✓ Supabase監視機能が有効です（30秒間隔で自動復旧）${NC}"
echo -e "${CYAN}フロントエンド: ${NC}http://localhost:5173"
echo -e "${CYAN}バックエンド: ${NC}http://localhost:8000"
echo -e "${CYAN}Supabase Studio: ${NC}http://localhost:54323"
echo -e "${BLUE}----------------------------------------${NC}"
echo -e "${YELLOW}終了するには Ctrl+C を押してください${NC}"

# すべてのバックグラウンドプロセスが終了するまで待機
wait 