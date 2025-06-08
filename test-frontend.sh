#!/bin/bash

# カラー設定
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
RESET='\033[0m'

echo -e "${BLUE}===== Techquiz Frontend Test Runner =====${RESET}"

# Node.jsバージョンの確認
if ! command -v node &> /dev/null; then
    echo -e "${RED}エラー: Node.jsがインストールされていません。${RESET}"
    echo -e "Node.jsをインストールしてから再試行してください。"
    exit 1
fi

NODE_VERSION=$(node -v)
echo -e "${BLUE}Node.jsバージョン: ${NODE_VERSION}${RESET}"

# 依存関係のインストール
echo -e "${BLUE}依存関係を確認・インストールしています...${RESET}"
npm install

# テストの種類を選択
echo -e "${BLUE}実行するテストの種類を選択してください：${RESET}"
echo "1) コンポーネントテスト"
echo "2) API統合テスト"
echo "3) すべてのテスト"
echo "4) カバレッジレポート生成"
read -p "選択（1-4）: " TEST_TYPE

case $TEST_TYPE in
    1)
        echo -e "${GREEN}===== コンポーネントテストを実行しています... =====${RESET}"
        npm test -- --selectProjects=component
        ;;
    2)
        echo -e "${GREEN}===== API統合テストを実行しています... =====${RESET}"
        npm test -- src/components/tests/QuizApiIntegration.test.ts
        ;;
    3)
        echo -e "${GREEN}===== すべてのテストを実行しています... =====${RESET}"
        npm test
        ;;
    4)
        echo -e "${GREEN}===== カバレッジレポートを生成しています... =====${RESET}"
        npm test -- --coverage
        ;;
    *)
        echo -e "${RED}無効な選択です。テストを中止します。${RESET}"
        exit 1
        ;;
esac

# テスト結果の確認
TEST_RESULT=$?
if [ $TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}すべてのテストが成功しました！${RESET}"
    
    # テスト結果まとめ
    echo -e "${GREEN}テスト概要:${RESET}"
    case $TEST_TYPE in
        1) echo "✓ コンポーネントテスト" ;;
        2) echo "✓ API統合テスト" ;;
        3) echo "✓ すべてのテスト" ;;
        4) echo "✓ カバレッジレポート生成" ;;
    esac
    
    # カバレッジレポートの表示（オプション4の場合）
    if [ "$TEST_TYPE" = "4" ]; then
        echo -e "${BLUE}カバレッジレポートは coverage/lcov-report/index.html で確認できます${RESET}"
    fi
else
    echo -e "${RED}テストに失敗しました。エラーを修正してください。${RESET}"
fi

exit $TEST_RESULT 