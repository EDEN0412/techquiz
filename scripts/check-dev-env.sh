#!/bin/bash

# カラー設定
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}🔍 開発環境ヘルスチェック${NC}"
echo -e "${BLUE}===========================${NC}"

# Docker状態チェック
echo -n "Docker デーモン: "
if docker info &> /dev/null; then
  echo -e "${GREEN}✓ 動作中${NC}"
else
  echo -e "${RED}✗ 停止中 - Dockerを起動してください${NC}"
  exit 1
fi

# Supabase状態チェック
echo -n "Supabase サービス: "
status_output=$(npx supabase status 2>/dev/null)

if echo "$status_output" | grep -q "API URL: http://127.0.0.1:54321"; then
  echo -e "${GREEN}✓ 動作中${NC}"
  echo -e "${BLUE}  API: http://127.0.0.1:54321${NC}"
  echo -e "${BLUE}  Studio: http://127.0.0.1:54323${NC}"
else
  echo -e "${YELLOW}⚠️  停止中 - 自動起動しますか？ (y/n)${NC}"
  read -r response
  if [[ "$response" =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Supabaseを起動中...${NC}"
    npx supabase start
    echo -e "${GREEN}✓ Supabaseが起動しました${NC}"
  else
    echo -e "${RED}Supabaseが停止したままです${NC}"
  fi
fi

# Node.js依存関係チェック
echo -n "Node.js 依存関係: "
if [ -d "node_modules" ]; then
  echo -e "${GREEN}✓ インストール済み${NC}"
else
  echo -e "${YELLOW}⚠️  未インストール - npm install を実行してください${NC}"
fi

# Python依存関係チェック（Poetry使用時）
echo -n "Python 依存関係: "
if command -v poetry &> /dev/null; then
  cd backend
  if poetry show &> /dev/null; then
    echo -e "${GREEN}✓ Poetry環境準備済み${NC}"
  else
    echo -e "${YELLOW}⚠️  Poetry環境未構築 - poetry install を実行してください${NC}"
  fi
  cd ..
else
  echo -e "${BLUE}ℹ️  Poetry未使用（通常のPython環境）${NC}"
fi

# 環境変数ファイルチェック
echo -n "環境変数ファイル: "
missing_files=()

if [ ! -f ".env.development" ]; then
  missing_files+=(".env.development")
fi

if [ ! -f "backend/.env" ]; then
  missing_files+=("backend/.env")
fi

if [ ${#missing_files[@]} -eq 0 ]; then
  echo -e "${GREEN}✓ 全て存在${NC}"
else
  echo -e "${RED}✗ 不足: ${missing_files[*]}${NC}"
  echo -e "${YELLOW}  .env.example ファイルをコピーして作成してください${NC}"
fi

echo -e "${BLUE}===========================${NC}"
echo -e "${GREEN}環境チェック完了！${NC}"

# 開発サーバー起動オプション
echo -e "${YELLOW}開発サーバーを起動しますか？ (y/n)${NC}"
read -r start_response
if [[ "$start_response" =~ ^[Yy]$ ]]; then
  echo -e "${GREEN}開発サーバーを起動中...${NC}"
  ./dev.sh
fi 