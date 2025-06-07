#!/bin/bash

# 色の定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}🔄 開発環境完全リセット${NC}"
echo -e "${BLUE}========================${NC}"

# 確認プロンプト
read -p "⚠️  開発環境を完全にリセットしますか？ (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
  echo -e "${YELLOW}リセットをキャンセルしました${NC}"
  exit 1
fi

# ステップ1: 全プロセスの停止
echo -e "\n${YELLOW}🛑 Step 1: 全プロセスの停止${NC}"

echo "  開発サーバープロセスを検索・停止中..."
# フロントエンド (Vite)
if lsof -i :5173 > /dev/null 2>&1; then
  echo "    フロントエンドサーバー (port 5173) を停止中..."
  lsof -ti :5173 | xargs kill -9 2>/dev/null
fi

# バックエンド (Django)
if lsof -i :8000 > /dev/null 2>&1; then
  echo "    バックエンドサーバー (port 8000) を停止中..."
  lsof -ti :8000 | xargs kill -9 2>/dev/null
fi

# Node.js プロセス
echo "    Node.js プロセスを停止中..."
pkill -f "vite" 2>/dev/null
pkill -f "node.*dev" 2>/dev/null

# Python/Django プロセス
echo "    Python/Django プロセスを停止中..."
pkill -f "python.*manage.py.*runserver" 2>/dev/null

echo -e "  ${GREEN}✓ プロセス停止完了${NC}"

# ステップ2: Supabaseの完全停止・クリーンアップ
echo -e "\n${YELLOW}🗄️  Step 2: Supabase完全リセット${NC}"

echo "  Supabaseサービスを停止中..."
npx supabase stop 2>/dev/null

echo "  Supabaseコンテナとボリュームをクリーンアップ中..."
# Supabase関連のDockerコンテナを停止・削除
docker ps -a | grep supabase | awk '{print $1}' | xargs docker rm -f 2>/dev/null

# Supabase関連のDockerボリュームを削除
docker volume ls | grep supabase | awk '{print $2}' | xargs docker volume rm 2>/dev/null

echo -e "  ${GREEN}✓ Supabase クリーンアップ完了${NC}"

# ステップ3: キャッシュとログのクリーンアップ
echo -e "\n${YELLOW}🧹 Step 3: キャッシュ・ログクリーンアップ${NC}"

# Node.js キャッシュ
if [ -d "node_modules/.vite" ]; then
  echo "  Viteキャッシュを削除中..."
  rm -rf node_modules/.vite
fi

if [ -d ".vite" ]; then
  echo "  .viteディレクトリを削除中..."
  rm -rf .vite
fi

# Django キャッシュ
if [ -d "backend/__pycache__" ]; then
  echo "  Django __pycache__ を削除中..."
  find backend -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
fi

if [ -d "backend/.pytest_cache" ]; then
  echo "  pytest キャッシュを削除中..."
  rm -rf backend/.pytest_cache
fi

# ログファイル
if [ -f "backend/debug.log" ]; then
  echo "  Django ログファイルを削除中..."
  rm -f backend/debug.log
fi

echo -e "  ${GREEN}✓ キャッシュクリーンアップ完了${NC}"

# ステップ4: Dockerのクリーンアップ
echo -e "\n${YELLOW}🐳 Step 4: Docker クリーンアップ${NC}"

echo "  未使用のDockerリソースをクリーンアップ中..."
docker system prune -f > /dev/null 2>&1

echo -e "  ${GREEN}✓ Docker クリーンアップ完了${NC}"

# ステップ5: 環境の再構築
echo -e "\n${YELLOW}🔧 Step 5: 環境再構築${NC}"

echo "  Supabaseを再初期化中..."
npx supabase start

echo "  環境変数を再チェック中..."
if [ ! -f ".env.development" ]; then
  echo -e "  ${YELLOW}⚠️  .env.development が見つかりません${NC}"
  echo "  .env.example から .env.development を作成してください"
fi

if [ ! -f "backend/.env" ]; then
  echo -e "  ${YELLOW}⚠️  backend/.env が見つかりません${NC}"
  echo "  backend/.env.example から backend/.env を作成してください"
fi

echo -e "  ${GREEN}✓ 環境再構築完了${NC}"

# ステップ6: 最終確認
echo -e "\n${YELLOW}🔍 Step 6: 最終確認${NC}"

# プリフライトチェックの実行
if [ -f "scripts/preflight-check.sh" ]; then
  echo "  プリフライトチェックを実行中..."
  chmod +x scripts/preflight-check.sh
  ./scripts/preflight-check.sh
else
  echo "  基本的なチェックを実行中..."
  
  # 基本チェック
  echo -n "    Node.js... "
  if command -v node > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
  else
    echo -e "${RED}✗${NC}"
  fi
  
  echo -n "    Python... "
  if command -v python > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
  else
    echo -e "${RED}✗${NC}"
  fi
  
  echo -n "    Docker... "
  if docker info > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
  else
    echo -e "${RED}✗${NC}"
  fi
  
  echo -n "    Supabase... "
  sleep 3  # Supabaseの起動を待つ
  if npx supabase status | grep -q "API URL: http://127.0.0.1:54321"; then
    echo -e "${GREEN}✓${NC}"
  else
    echo -e "${RED}✗${NC}"
  fi
fi

echo -e "\n${BLUE}========================${NC}"
echo -e "${GREEN}🎉 環境リセット完了！${NC}"
echo -e "\n${CYAN}次のステップ:${NC}"
echo -e "  1. ${YELLOW}./dev.sh${NC} で開発環境を起動"
echo -e "  2. ${YELLOW}./scripts/health-check.sh${NC} で状態確認"
echo -e "\n${CYAN}利用可能なURL:${NC}"
echo -e "  フロントエンド: ${CYAN}http://localhost:5173${NC}"
echo -e "  バックエンド: ${CYAN}http://localhost:8000${NC}" 
echo -e "  Supabase Studio: ${CYAN}http://localhost:54323${NC}" 