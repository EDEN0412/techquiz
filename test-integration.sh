#!/bin/bash

# カラー設定
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
RESET='\033[0m'

echo -e "${BLUE}===== Techquiz 結合テスト実行ツール =====${RESET}"

# テスト実行の確認
read -p "バックエンドとフロントエンドの両方の結合テストを実行しますか？ (y/n): " RUN_TESTS
if [ "$RUN_TESTS" != "y" ]; then
    echo -e "${YELLOW}テストがキャンセルされました。${RESET}"
    exit 0
fi

# スクリプトの存在確認
if [ ! -f "./backend/test.sh" ]; then
    echo -e "${RED}エラー: backend/test.sh が見つかりません。${RESET}"
    exit 1
fi

if [ ! -f "./test-frontend.sh" ]; then
    echo -e "${RED}エラー: test-frontend.sh が見つかりません。${RESET}"
    exit 1
fi

# バックエンドサービスの起動
echo -e "${BLUE}バックエンドサービスを起動しています...${RESET}"
cd backend
python manage.py runserver 8000 &
BACKEND_PID=$!

# バックエンドの起動を待機
echo -e "${YELLOW}バックエンドサービスの起動を待機しています (5秒)...${RESET}"
sleep 5

# バックエンドテストの実行
echo -e "${GREEN}========== バックエンド結合テスト ==========${RESET}"
./test.sh

BACKEND_TEST_RESULT=$?

# フロントエンドテストの実行
echo -e "${GREEN}========== フロントエンド結合テスト ==========${RESET}"
cd ..
./test-frontend.sh

FRONTEND_TEST_RESULT=$?

# バックエンドサービスの停止
echo -e "${BLUE}バックエンドサービスを停止しています...${RESET}"
kill $BACKEND_PID

# テスト結果の表示
echo -e "${BLUE}===== テスト結果サマリー =====${RESET}"
if [ $BACKEND_TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}バックエンドテスト: 成功${RESET}"
else
    echo -e "${RED}バックエンドテスト: 失敗${RESET}"
fi

if [ $FRONTEND_TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}フロントエンドテスト: 成功${RESET}"
else
    echo -e "${RED}フロントエンドテスト: 失敗${RESET}"
fi

# 終了ステータス
if [ $BACKEND_TEST_RESULT -eq 0 ] && [ $FRONTEND_TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}すべてのテストが成功しました！${RESET}"
    exit 0
else
    echo -e "${RED}一部のテストが失敗しました。詳細なログを確認してください。${RESET}"
    exit 1
fi 