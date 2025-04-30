#!/bin/bash

# カラー設定
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# タイトル表示
echo -e "${YELLOW}====================================${NC}"
echo -e "${YELLOW}     Techquiz テスト実行ツール     ${NC}"
echo -e "${YELLOW}====================================${NC}"

# 現在のディレクトリを確認
if [[ $(basename $(pwd)) != "backend" ]]; then
  if [[ -d "./backend" ]]; then
    cd backend
    echo -e "${YELLOW}ディレクトリをbackendに変更しました${NC}"
  else
    echo -e "${RED}エラー: backendディレクトリが見つかりません${NC}"
    echo -e "${YELLOW}このスクリプトはプロジェクトのルートディレクトリかbackendディレクトリから実行してください${NC}"
    exit 1
  fi
fi

# 環境変数の設定
echo -e "${YELLOW}テスト環境を設定しています...${NC}"
export DJANGO_SETTINGS_MODULE="techskillsquiz.settings.test"

# 引数の解析
PYTEST_ARGS=""
COVERAGE=false
VERBOSE=false

for arg in "$@"; do
  case $arg in
    --coverage)
      COVERAGE=true
      ;;
    -v|--verbose)
      VERBOSE=true
      PYTEST_ARGS="$PYTEST_ARGS -v"
      ;;
    *)
      PYTEST_ARGS="$PYTEST_ARGS $arg"
      ;;
  esac
done

# テスト実行コマンドの構築
if [ "$COVERAGE" = true ]; then
  echo -e "${YELLOW}カバレッジレポート付きでテストを実行します${NC}"
  TEST_CMD="python -m pytest --cov=. --cov-report=term --cov-report=html:coverage_report $PYTEST_ARGS"
else
  if [ "$VERBOSE" = true ]; then
    echo -e "${YELLOW}詳細モードでテストを実行します${NC}"
  else
    echo -e "${YELLOW}テストを実行します${NC}"
  fi
  TEST_CMD="python -m pytest $PYTEST_ARGS"
fi

# テスト実行
echo -e "${YELLOW}コマンド: $TEST_CMD${NC}"
eval $TEST_CMD
TEST_RESULT=$?

# 結果の表示
if [ $TEST_RESULT -eq 0 ]; then
  echo -e "${GREEN}テストが正常に完了しました！${NC}"
  
  if [ "$COVERAGE" = true ]; then
    echo -e "${YELLOW}カバレッジレポートは coverage_report ディレクトリに生成されました${NC}"
    echo -e "${YELLOW}ブラウザで coverage_report/index.html を開いて確認できます${NC}"
  fi
else
  echo -e "${RED}テストで問題が発生しました${NC}"
fi

exit $TEST_RESULT 