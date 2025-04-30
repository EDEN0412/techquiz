#!/bin/bash

# テスト実行用スクリプト
# 使い方: ./test.sh [テストパス]
# 例: ./test.sh                          # 全テストを実行
# 例: ./test.sh backend/tests/           # 特定のディレクトリのテストを実行
# 例: ./test.sh backend/tests/test_*.py  # 特定のパターンのテストを実行

# エラー発生時に停止
set -e

# 必要なPythonパスを設定
export PYTHONPATH=$PYTHONPATH:$(pwd)/backend

# 環境変数を設定
export DJANGO_SETTINGS_MODULE=techskillsquiz.settings.test

# 表示色の設定
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}テスト実行を開始します...${NC}"

# 引数がある場合はそのテストを実行、なければ全テストを実行
if [ $# -eq 0 ]; then
    echo -e "${BLUE}全テストを実行します${NC}"
    pytest -xvs backend/
else
    echo -e "${BLUE}指定されたテストを実行します: $1${NC}"
    pytest -xvs "$@"
fi

# 終了コードを取得
EXIT_CODE=$?

# 結果に応じてメッセージを表示
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}テストが正常に完了しました！${NC}"
else
    echo -e "${RED}テストに失敗しました。${NC}"
fi

exit $EXIT_CODE 