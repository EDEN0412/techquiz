-- 不足している主要テーブルを作成するマイグレーション
-- 作成日: 2025-01-18

-- Django認証システムのユーザーテーブル
CREATE TABLE IF NOT EXISTS auth_user (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMPTZ,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL DEFAULT '',
    last_name VARCHAR(150) NOT NULL DEFAULT '',
    email VARCHAR(254) NOT NULL DEFAULT '',
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Django認証システムのグループテーブル
CREATE TABLE IF NOT EXISTS auth_group (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
);

-- Django認証システムの権限テーブル
CREATE TABLE IF NOT EXISTS auth_permission (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL,
    codename VARCHAR(100) NOT NULL
);

-- Django認証システムのユーザーグループ関連テーブル
CREATE TABLE IF NOT EXISTS auth_user_groups (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    UNIQUE(user_id, group_id)
);

-- Django認証システムのユーザー権限関連テーブル
CREATE TABLE IF NOT EXISTS auth_user_user_permissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    UNIQUE(user_id, permission_id)
);

-- Django content typesテーブル
CREATE TABLE IF NOT EXISTS django_content_type (
    id SERIAL PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    UNIQUE(app_label, model)
);

-- Django sessionsテーブル
CREATE TABLE IF NOT EXISTS django_session (
    session_key VARCHAR(40) PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date TIMESTAMPTZ NOT NULL
);

-- Django migrationsテーブル
CREATE TABLE IF NOT EXISTS django_migrations (
    id SERIAL PRIMARY KEY,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- クイズ関連テーブル（既にcategoryは存在するのでスキップ）

-- 難易度レベルテーブル（既存の場合はスキップ）
CREATE TABLE IF NOT EXISTS quiz_difficultylevel (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    slug VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    level INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- クイズテーブル
CREATE TABLE IF NOT EXISTS quiz_quiz (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category_id INTEGER NOT NULL,
    difficulty_level_id INTEGER NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 質問テーブル
CREATE TABLE IF NOT EXISTS quiz_question (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    explanation TEXT,
    hint TEXT,
    order_index INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 回答選択肢テーブル
CREATE TABLE IF NOT EXISTS quiz_answer (
    id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL,
    answer_text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL DEFAULT FALSE,
    order_index INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- クイズ結果テーブル
CREATE TABLE IF NOT EXISTS quiz_quizresult (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    quiz_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    total_questions INTEGER NOT NULL,
    time_taken INTEGER, -- 秒数
    completed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ユーザー統計テーブル
CREATE TABLE IF NOT EXISTS quiz_userstatistics (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL UNIQUE,
    total_quizzes_completed INTEGER NOT NULL DEFAULT 0,
    total_questions_answered INTEGER NOT NULL DEFAULT 0,
    total_correct_answers INTEGER NOT NULL DEFAULT 0,
    average_score DECIMAL(5,2) NOT NULL DEFAULT 0.00,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 活動履歴テーブル
CREATE TABLE IF NOT EXISTS quiz_activityhistory (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    quiz_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    completed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- JWT トークンブラックリスト関連テーブル
CREATE TABLE IF NOT EXISTS token_blacklist_outstandingtoken (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    jti VARCHAR(255) NOT NULL UNIQUE,
    token TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE IF NOT EXISTS token_blacklist_blacklistedtoken (
    id SERIAL PRIMARY KEY,
    token_id INTEGER NOT NULL UNIQUE,
    blacklisted_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- インデックスの作成
CREATE INDEX IF NOT EXISTS auth_user_username_idx ON auth_user(username);
CREATE INDEX IF NOT EXISTS auth_user_email_idx ON auth_user(email);
CREATE INDEX IF NOT EXISTS quiz_quiz_category_id_idx ON quiz_quiz(category_id);
CREATE INDEX IF NOT EXISTS quiz_quiz_difficulty_level_id_idx ON quiz_quiz(difficulty_level_id);
CREATE INDEX IF NOT EXISTS quiz_question_quiz_id_idx ON quiz_question(quiz_id);
CREATE INDEX IF NOT EXISTS quiz_answer_question_id_idx ON quiz_answer(question_id);
CREATE INDEX IF NOT EXISTS quiz_quizresult_user_id_idx ON quiz_quizresult(user_id);
CREATE INDEX IF NOT EXISTS quiz_quizresult_quiz_id_idx ON quiz_quizresult(quiz_id);
CREATE INDEX IF NOT EXISTS quiz_activityhistory_user_id_idx ON quiz_activityhistory(user_id);
CREATE INDEX IF NOT EXISTS django_session_expire_date_idx ON django_session(expire_date);

-- 外部キー制約の追加（参照整合性）
-- 注意: 既存データがある場合は制約追加が失敗する可能性があるため、IF NOT EXISTSは使用できません
-- 必要に応じて手動で追加してください

COMMENT ON TABLE auth_user IS 'Django認証システムのユーザーテーブル';
COMMENT ON TABLE quiz_quiz IS 'クイズの基本情報テーブル';
COMMENT ON TABLE quiz_question IS 'クイズの質問テーブル';
COMMENT ON TABLE quiz_answer IS '質問の回答選択肢テーブル';
COMMENT ON TABLE quiz_quizresult IS 'ユーザーのクイズ結果テーブル';
COMMENT ON TABLE quiz_userstatistics IS 'ユーザーの統計情報テーブル';
COMMENT ON TABLE quiz_activityhistory IS 'ユーザーの活動履歴テーブル'; 