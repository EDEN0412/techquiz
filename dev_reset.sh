#!/usr/bin/env bash
# 開発用：Supabase DB をスキーマのみリセットし、Django マイグレーションを適用してからシードを流し込む
# これ一発で **パターンA** 手順を再現できます
set -euo pipefail

RUNNING=0
if npx supabase status >/dev/null 2>&1; then
  RUNNING=1
fi

# 1a. 停止してクリーンにする
if [ $RUNNING -eq 1 ]; then
  echo "[dev_reset] supabase stop"
  npx supabase stop || true
fi

# 1b. 起動（この時点ではDBは空）
echo "[dev_reset] supabase start"
set +e
npx supabase start
START_EXIT=$?
if [ $START_EXIT -ne 0 ]; then
  echo "[dev_reset] supabase start failed (code=$START_EXIT). Retrying once after forced stop..."
  npx supabase stop || true
  sleep 2
  npx supabase start
  START_EXIT=$?
fi
set -e
if [ $START_EXIT -ne 0 ]; then
  echo "[dev_reset] supabase start failed twice. Please run 'supabase start --debug' manually to inspect issues." >&2
  exit $START_EXIT
fi

# 2. DB を空状態に（シードは行わない）
echo "[dev_reset] supabase db reset --no-seed --local"
set +e
yes | npx supabase db reset --no-seed --local || RESET_EXIT=$?
if [ "${RESET_EXIT:-0}" -ne 0 ]; then
  echo "[dev_reset] db reset failed, trying once more after 5s..."
  sleep 5
  yes | npx supabase db reset --no-seed --local
fi
set -e
# supabase CLI が 502 で終了してもコンテナは作成済みことがあるためリカバリ
if [ $RESET_EXIT -ne 0 ]; then
  echo "[dev_reset] supabase reset exited with code $RESET_EXIT — attempting to restart containers"
  npx supabase start
fi

# 3. Django マイグレーション適用
echo "[dev_reset] django migrate"
(cd backend && DJANGO_ENV=development python manage.py migrate --noinput)

# 3.5. NULL を許容しない追加カラムにデフォルト値を設定（seed の簡略化）
echo "[dev_reset] add defaults to quiz_question / quiz_answer"
docker exec -i supabase_db_techquiz psql -U postgres -d postgres <<'SQL'
ALTER TABLE quiz_question ALTER COLUMN code_snippet SET DEFAULT '';
ALTER TABLE quiz_question ALTER COLUMN image_url SET DEFAULT '';
ALTER TABLE quiz_question ALTER COLUMN media_type SET DEFAULT 'none';
ALTER TABLE quiz_question ALTER COLUMN syntax_highlight SET DEFAULT '';
ALTER TABLE quiz_question ALTER COLUMN updated_at SET DEFAULT NOW();

ALTER TABLE quiz_answer ALTER COLUMN feedback SET DEFAULT '';
ALTER TABLE quiz_answer ALTER COLUMN updated_at SET DEFAULT NOW();

ALTER TABLE quiz_quiz ALTER COLUMN updated_at SET DEFAULT NOW();
SQL

# 4. 初期データ投入（カテゴリ・難易度・クイズ問題など）
echo "[dev_reset] seeding data (supabase/seed.sql)"
cat supabase/seed.sql | docker exec -i supabase_db_techquiz psql -U postgres -d postgres

echo "[dev_reset] ✅ 完了" 