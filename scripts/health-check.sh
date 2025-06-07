#!/bin/bash

# 色の定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ヘルスチェック関数
check_service() {
  local service_name="$1"
  local check_command="$2"
  local url="$3"
  
  echo -n "  $service_name... "
  
  if eval "$check_command" > /dev/null 2>&1; then
    echo -e "${GREEN}✓ 正常${NC}"
    [ -n "$url" ] && echo -e "    ${CYAN}→ $url${NC}"
    return 0
  else
    echo -e "${RED}✗ 停止${NC}"
    return 1
  fi
}

# APIエンドポイントのチェック
check_api_endpoint() {
  local service_name="$1"
  local url="$2"
  local expected_status="$3"
  
  echo -n "  $service_name API... "
  
  local status_code=$(curl -s -o /dev/null -w "%{http_code}" "$url" 2>/dev/null)
  
  if [ "$status_code" = "$expected_status" ]; then
    echo -e "${GREEN}✓ HTTP $status_code${NC}"
    echo -e "    ${CYAN}→ $url${NC}"
    return 0
  else
    echo -e "${RED}✗ HTTP $status_code${NC}"
    return 1
  fi
}

echo -e "${CYAN}🏥 開発環境ヘルスチェック${NC}"
echo -e "${BLUE}========================${NC}"

# サービス稼働チェック
echo -e "\n${YELLOW}🔧 サービス稼働状況${NC}"

# フロントエンド
check_service "フロントエンド (Vite)" "lsof -i :5173" "http://localhost:5173"

# バックエンド  
check_service "バックエンド (Django)" "lsof -i :8000" "http://localhost:8000"

# Supabase
check_service "Supabase API" "lsof -i :54321" "http://localhost:54321"
check_service "Supabase Studio" "lsof -i :54323" "http://localhost:54323"
check_service "Supabase DB" "lsof -i :54322" "postgresql://postgres:postgres@localhost:54322/postgres"

# APIエンドポイントチェック
echo -e "\n${YELLOW}🌐 APIエンドポイント確認${NC}"

# Django API
check_api_endpoint "Django Admin" "http://localhost:8000/admin/" "200"
check_api_endpoint "Django API Root" "http://localhost:8000/api/v1/" "200"
check_api_endpoint "Django Auth API" "http://localhost:8000/api/v1/users/" "401"

# Supabase API
check_api_endpoint "Supabase Health" "http://localhost:54321/health" "200"
check_api_endpoint "Supabase Rest API" "http://localhost:54321/rest/v1/" "200"

# データベース接続確認
echo -e "\n${YELLOW}🗄️  データベース接続確認${NC}"

# Django DB接続
echo -n "  Django → Database... "
if cd backend && python -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'techskillsquiz.settings')
django.setup()
from django.db import connection
cursor = connection.cursor()
cursor.execute('SELECT 1')
print('OK')
" 2>/dev/null; then
  echo -e "${GREEN}✓ 接続成功${NC}"
else
  echo -e "${RED}✗ 接続失敗${NC}"
fi
cd ..

# Supabase DB接続
echo -n "  Supabase Database... "
if psql postgresql://postgres:postgres@localhost:54322/postgres -c "SELECT 1;" > /dev/null 2>&1; then
  echo -e "${GREEN}✓ 接続成功${NC}"
else
  echo -e "${RED}✗ 接続失敗${NC}"
fi

# 環境変数確認
echo -e "\n${YELLOW}⚙️  環境変数確認${NC}"

check_env_file() {
  local file_path="$1"
  local file_name="$2"
  
  echo -n "  $file_name... "
  if [ -f "$file_path" ]; then
    echo -e "${GREEN}✓ 存在${NC}"
  else
    echo -e "${RED}✗ 不存在${NC}"
  fi
}

check_env_file ".env.development" "Frontend Environment"
check_env_file "backend/.env" "Backend Environment"
check_env_file "supabase/config.toml" "Supabase Config"

# 実行時間の記録
echo -e "\n${BLUE}========================${NC}"
echo -e "${CYAN}📊 チェック完了時刻: $(date '+%Y-%m-%d %H:%M:%S')${NC}"

# 自動修復の提案
echo -e "\n${YELLOW}🔧 自動修復オプション:${NC}"
echo -e "  ${CYAN}全サービス再起動:${NC} ./dev.sh"
echo -e "  ${CYAN}Supabaseのみ再起動:${NC} npx supabase restart"
echo -e "  ${CYAN}完全環境リセット:${NC} ./scripts/reset-env.sh" 