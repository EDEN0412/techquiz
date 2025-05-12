#!/bin/bash

# カラー設定
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
RESET='\033[0m'

echo -e "${BLUE}===== Techquiz Backend Test Runner =====${RESET}"

# 環境変数ファイルの確認
ENV_FILE=".env.test"
if [ ! -f "$ENV_FILE" ]; then
    echo -e "${RED}エラー: .env.test ファイルが見つかりません。${RESET}"
    echo -e "${YELLOW}ファイルを作成するか、.env.example をコピーしてください。${RESET}"
    exit 1
fi

# 仮想環境の検証
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}警告: 仮想環境が検出されませんでした。${RESET}"
    echo -e "仮想環境を作成して有効化することをお勧めします："
    echo -e "  python -m venv venv"
    echo -e "  source venv/bin/activate (Linuxの場合)"
    echo -e "  .\\venv\\Scripts\\activate (Windowsの場合)"
    
    # 続行するか確認
    read -p "仮想環境なしで続行しますか？ (y/n): " CONTINUE
    if [ "$CONTINUE" != "y" ]; then
        echo -e "${RED}テストが中止されました。${RESET}"
        exit 1
    fi
fi

# 必要なパッケージがインストールされているか確認
echo -e "${BLUE}依存パッケージを確認しています...${RESET}"
python -m pip install -r requirements-test.txt

# Djangoが必要とする環境変数を設定
export DJANGO_SETTINGS_MODULE=techskillsquiz.settings.test

# テストの種類を選択
echo -e "${BLUE}実行するテストの種類を選択してください：${RESET}"
echo "1) 単体テスト（モデル、シリアライザーなど）"
echo "2) API・ビューテスト"
echo "3) 統合テスト（フロントエンド・バックエンド結合）"
echo "4) フロントエンドAPIクライアントモックテスト"
echo "5) すべてのテスト"
read -p "選択（1-5）: " TEST_TYPE

# テストディレクトリ
TEST_DIR="quiz/tests"

# カバレッジレポート用の設定
COVERAGE_COMMAND="python -m pytest"
COVERAGE_OPTS="--cov=quiz --cov-report=term --cov-report=html"

case $TEST_TYPE in
    1)
        echo -e "${GREEN}===== 単体テストを実行しています... =====${RESET}"
        ${COVERAGE_COMMAND} ${TEST_DIR}/test_models.py ${TEST_DIR}/test_serializers.py ${COVERAGE_OPTS}
        ;;
    2)
        echo -e "${GREEN}===== APIテストを実行しています... =====${RESET}"
        ${COVERAGE_COMMAND} ${TEST_DIR}/test_views.py ${COVERAGE_OPTS}
        ;;
    3)
        echo -e "${GREEN}===== 統合テストを実行しています... =====${RESET}"
        ${COVERAGE_COMMAND} ${TEST_DIR}/test_integration.py ${COVERAGE_OPTS}
        ;;
    4)
        echo -e "${GREEN}===== フロントエンドAPIクライアントモックテストを実行しています... =====${RESET}"
        ${COVERAGE_COMMAND} ${TEST_DIR}/test_api_client_mock.py ${COVERAGE_OPTS}
        ;;
    5)
        echo -e "${GREEN}===== すべてのテストを実行しています... =====${RESET}"
        ${COVERAGE_COMMAND} ${TEST_DIR} ${COVERAGE_OPTS}
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
    
    # カバレッジレポートの表示
    echo -e "${BLUE}カバレッジレポートは htmlcov/index.html で確認できます${RESET}"
    
    # テスト結果まとめ
    echo -e "${GREEN}テスト概要:${RESET}"
    case $TEST_TYPE in
        1) echo "✓ 単体テスト" ;;
        2) echo "✓ APIテスト" ;;
        3) echo "✓ 統合テスト" ;;
        4) echo "✓ フロントエンドAPIクライアントモックテスト" ;;
        5) echo "✓ すべてのテスト" ;;
    esac
else
    echo -e "${RED}テストに失敗しました。エラーを修正してください。${RESET}"
fi

exit $TEST_RESULT 