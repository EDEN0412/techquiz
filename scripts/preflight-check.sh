#!/bin/bash

# 色の定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}🔍 開発環境プリフライトチェック${NC}"
echo -e "${BLUE}================================${NC}"

# チェック結果をカウント
TOTAL_CHECKS=0
PASSED_CHECKS=0
ISSUES=()

# チェック関数
check_item() {
  local item_name="$1"
  local command="$2"
  local error_message="$3"
  
  TOTAL_CHECKS=$((TOTAL_CHECKS + 1))
  echo -n "  $item_name... "
  
  if eval "$command" > /dev/null 2>&1; then
    echo -e "${GREEN}✓${NC}"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
    return 0
  else
    echo -e "${RED}✗${NC}"
    ISSUES+=("$error_message")
    return 1
  fi
}

# 必須ツールの確認
echo -e "${YELLOW}🛠️  必須ツールの確認${NC}"
check_item "Node.js" "command -v node" "Node.js がインストールされていません"
check_item "npm" "command -v npm" "npm がインストールされていません"
check_item "Python" "command -v python" "Python がインストールされていません"
check_item "Docker" "command -v docker" "Docker がインストールされていません"
check_item "Docker Daemon" "docker info" "Docker デーモンが実行されていません"

# 依存関係の確認
echo -e "\n${YELLOW}📦 依存関係の確認${NC}"
check_item "Frontend dependencies" "[ -d node_modules ]" "npm install を実行してください"
check_item "Backend dependencies" "[ -f backend/.env ]" "backend/.env ファイルが見つかりません"
check_item "Environment file" "[ -f .env.development ]" ".env.development ファイルが見つかりません"

# Supabase環境の確認
echo -e "\n${YELLOW}🗄️  Supabase環境の確認${NC}"
check_item "Supabase CLI" "npx supabase --version" "Supabase CLI がインストールされていません"
check_item "Supabase config" "[ -f supabase/config.toml ]" "Supabase プロジェクトが初期化されていません"

# ポートの確認
echo -e "\n${YELLOW}🔌 ポート使用状況の確認${NC}"
check_item "Port 5173 (Frontend)" "! lsof -i :5173" "ポート 5173 が使用中です"
check_item "Port 8000 (Backend)" "! lsof -i :8000" "ポート 8000 が使用中です"
check_item "Port 54321 (Supabase API)" "! lsof -i :54321" "ポート 54321 が使用中です"
check_item "Port 54323 (Supabase Studio)" "! lsof -i :54323" "ポート 54323 が使用中です"

# Supabaseサービスの確認
echo -e "\n${YELLOW}⚡ Supabaseサービスの確認${NC}"
if npx supabase status > /dev/null 2>&1; then
  if npx supabase status | grep -q "API URL: http://127.0.0.1:54321"; then
    echo -e "  Supabase サービス... ${GREEN}✓${NC}"
    PASSED_CHECKS=$((PASSED_CHECKS + 1))
  else
    echo -e "  Supabase サービス... ${YELLOW}⚠️${NC}"
    ISSUES+=("Supabase は起動していますが、一部のサービスに問題があります")
  fi
else
  echo -e "  Supabase サービス... ${RED}✗${NC}"
  ISSUES+=("Supabase サービスが停止しています")
fi
TOTAL_CHECKS=$((TOTAL_CHECKS + 1))

# 結果の表示
echo -e "\n${BLUE}================================${NC}"
echo -e "${CYAN}📊 チェック結果${NC}"
echo -e "合格: ${GREEN}${PASSED_CHECKS}${NC}/${TOTAL_CHECKS}"

if [ ${#ISSUES[@]} -eq 0 ]; then
  echo -e "\n${GREEN}🎉 全てのチェックに合格しました！${NC}"
  echo -e "${GREEN}開発環境は正常に動作する準備ができています。${NC}"
  exit 0
else
  echo -e "\n${RED}❌ 以下の問題が見つかりました:${NC}"
  for issue in "${ISSUES[@]}"; do
    echo -e "  ${RED}•${NC} $issue"
  done
  
  echo -e "\n${YELLOW}💡 解決方法:${NC}"
  echo -e "  1. 上記の問題を解決してください"
  echo -e "  2. 解決後、再度このスクリプトを実行してください"
  echo -e "  3. 全てのチェックに合格したら ./dev.sh を実行してください"
  
  exit 1
fi 