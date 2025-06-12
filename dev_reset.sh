#!/usr/bin/env bash
# 開発用：Supabase DB をスキーマのみリセットし、Django マイグレーションを適用してからシードを流し込む
# これ一発で **パターンA** 手順を再現できます
set -euo pipefail

# Supabase CLI コマンド検出
if command -v supabase >/dev/null 2>&1; then
  SPBASE="supabase"
else
  SPBASE="npx supabase"
fi

RUNNING=0
if $SPBASE status >/dev/null 2>&1; then
  RUNNING=1
fi

# 1a. 停止してクリーンにする
if [ $RUNNING -eq 1 ]; then
  echo "[dev_reset] supabase stop"
  $SPBASE stop || true
fi

# 1b. 起動（この時点ではDBは空）
echo "[dev_reset] supabase start"
set +e
$SPBASE start
START_EXIT=$?
if [ $START_EXIT -ne 0 ]; then
  echo "[dev_reset] supabase start failed (code=$START_EXIT). Retrying once after forced stop..."
  $SPBASE stop || true
  sleep 2
  $SPBASE start
  START_EXIT=$?
fi
set -e
if [ $START_EXIT -ne 0 ]; then
  echo "[dev_reset] supabase start failed twice. Please run 'supabase start --debug' manually to inspect issues." >&2
  exit $START_EXIT
fi

# 2.5. DB コンテナが起動完了するまで待機（CI では即 exec すると失敗するため）
echo "[dev_reset] waiting for supabase_db_techquiz to be healthy..."
for i in {1..30}; do
  if docker ps --format '{{.Names}}' | grep -q '^supabase_db_techquiz$'; then
    if docker exec supabase_db_techquiz pg_isready -U postgres -d postgres >/dev/null 2>&1; then
      echo "[dev_reset] database is ready"
      break
    fi
  fi
  echo "[dev_reset] ...waiting ($i)"
  sleep 2
  if [ $i -eq 30 ]; then
    echo "[dev_reset] database did not become ready in time" >&2
    exit 1
  fi
done

# 2. DB を空状態に（シードは行わない）
echo "[dev_reset] supabase db reset --no-seed --local"
set +e
yes | $SPBASE db reset --no-seed --local || RESET_EXIT=$?
if [ "${RESET_EXIT:-0}" -ne 0 ]; then
  echo "[dev_reset] db reset failed, trying once more after 5s..."
  sleep 5
  yes | $SPBASE db reset --no-seed --local
fi
set -e
# supabase CLI が 502 で終了してもコンテナは作成済みことがあるためリカバリ
if [ $RESET_EXIT -ne 0 ]; then
  echo "[dev_reset] supabase reset exited with code $RESET_EXIT — attempting to restart containers"
  $SPBASE start
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