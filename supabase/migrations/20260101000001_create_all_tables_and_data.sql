-- 全テーブル作成と初期データ投入マイグレーション
-- 作成日: 2025-01-18

BEGIN;

-- =========================================================
-- 0. 既存テーブルの削除（冪等性確保のため）
-- =========================================================
DROP TABLE IF EXISTS quiz_activityhistory CASCADE;
DROP TABLE IF EXISTS quiz_userstatistics CASCADE;
DROP TABLE IF EXISTS quiz_quizresult CASCADE;
DROP TABLE IF EXISTS quiz_answer CASCADE;
DROP TABLE IF EXISTS quiz_question CASCADE;
DROP TABLE IF EXISTS quiz_quiz CASCADE;
DROP TABLE IF EXISTS quiz_difficultylevel CASCADE;
DROP TABLE IF EXISTS quiz_category CASCADE;
DROP TABLE IF EXISTS token_blacklist_blacklistedtoken CASCADE;
DROP TABLE IF EXISTS token_blacklist_outstandingtoken CASCADE;
DROP TABLE IF EXISTS django_session CASCADE;
DROP TABLE IF EXISTS django_content_type CASCADE;
DROP TABLE IF EXISTS auth_user_user_permissions CASCADE;
DROP TABLE IF EXISTS auth_user_groups CASCADE;
DROP TABLE IF EXISTS auth_permission CASCADE;
DROP TABLE IF EXISTS auth_group CASCADE;
DROP TABLE IF EXISTS auth_user CASCADE;
-- django_migrations は削除しない

-- =========================================================
-- 1. テーブル作成
-- =========================================================

-- Django認証システムのユーザーテーブル
CREATE TABLE auth_user (
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
CREATE TABLE auth_group (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
);

-- Django認証システムの権限テーブル
CREATE TABLE auth_permission (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL,
    codename VARCHAR(100) NOT NULL
);

-- Django認証システムのユーザーグループ関連テーブル
CREATE TABLE auth_user_groups (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    UNIQUE(user_id, group_id)
);

-- Django認証システムのユーザー権限関連テーブル
CREATE TABLE auth_user_user_permissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    UNIQUE(user_id, permission_id)
);

-- Django content typesテーブル
CREATE TABLE django_content_type (
    id SERIAL PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL,
    UNIQUE(app_label, model)
);

-- Django sessionsテーブル
CREATE TABLE django_session (
    session_key VARCHAR(40) PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date TIMESTAMPTZ NOT NULL
);

-- Django migrationsテーブルはSupabaseが管理するため、ここでは作成しない

-- カテゴリテーブル
CREATE TABLE quiz_category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    icon VARCHAR(50),
    display_order INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 難易度レベルテーブル
CREATE TABLE quiz_difficultylevel (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    slug VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    level INTEGER NOT NULL,
    point_multiplier INTEGER NOT NULL DEFAULT 1,
    time_limit INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- クイズテーブル
CREATE TABLE quiz_quiz (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    category_id INTEGER NOT NULL,
    difficulty_id INTEGER NOT NULL,
    time_limit INTEGER,
    pass_score INTEGER NOT NULL DEFAULT 70,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    thumbnail_url TEXT,
    banner_image_url TEXT,
    media_type VARCHAR(20) NOT NULL DEFAULT 'none',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 質問テーブル
CREATE TABLE quiz_question (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL DEFAULT 'multiple_choice',
    explanation TEXT,
    hint TEXT,
    points INTEGER NOT NULL DEFAULT 1,
    display_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 回答選択肢テーブル
CREATE TABLE quiz_answer (
    id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL,
    answer_text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL DEFAULT FALSE,
    display_order INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- クイズ結果テーブル
CREATE TABLE quiz_quizresult (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    quiz_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    total_questions INTEGER NOT NULL,
    time_taken INTEGER,
    completed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ユーザー統計テーブル
CREATE TABLE quiz_userstatistics (
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
CREATE TABLE quiz_activityhistory (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    quiz_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    completed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- JWT トークンブラックリスト関連テーブル
CREATE TABLE token_blacklist_outstandingtoken (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    jti VARCHAR(255) NOT NULL UNIQUE,
    token TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at TIMESTAMPTZ NOT NULL
);

CREATE TABLE token_blacklist_blacklistedtoken (
    id SERIAL PRIMARY KEY,
    token_id INTEGER NOT NULL UNIQUE,
    blacklisted_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- =========================================================
-- 2. インデックス作成
-- =========================================================

CREATE INDEX auth_user_username_idx ON auth_user(username);
CREATE INDEX auth_user_email_idx ON auth_user(email);
CREATE INDEX quiz_quiz_category_id_idx ON quiz_quiz(category_id);
CREATE INDEX quiz_quiz_difficulty_id_idx ON quiz_quiz(difficulty_id);
CREATE INDEX quiz_question_quiz_id_idx ON quiz_question(quiz_id);
CREATE INDEX quiz_answer_question_id_idx ON quiz_answer(question_id);
CREATE INDEX quiz_quizresult_user_id_idx ON quiz_quizresult(user_id);
CREATE INDEX quiz_quizresult_quiz_id_idx ON quiz_quizresult(quiz_id);
CREATE INDEX quiz_activityhistory_user_id_idx ON quiz_activityhistory(user_id);
CREATE INDEX django_session_expire_date_idx ON django_session(expire_date);

-- =========================================================
-- 3. 初期データ投入
-- =========================================================

-- カテゴリ挿入
INSERT INTO quiz_category (name, slug, description, icon, display_order, is_active, created_at, updated_at)
VALUES
('HTML & CSS', 'html-css', 'Webの基礎とスタイリングを習得', 'html', 1, true, NOW(), NOW()),
('Ruby', 'ruby', 'オブジェクト指向スクリプト言語の基礎', 'ruby', 2, true, NOW(), NOW()),
('Ruby on Rails', 'ruby-rails', 'Rubyベースの高速Webアプリケーション開発', 'rails', 3, true, NOW(), NOW()),
('JavaScript', 'javascript', 'Web開発に不可欠なプログラミング言語', 'javascript', 4, true, NOW(), NOW()),
('Webアプリケーション基礎', 'web-app-basic', 'Webアプリ開発の基礎知識とアーキテクチャ', 'web', 5, true, NOW(), NOW()),
('Python', 'python', '汎用性の高い読みやすいプログラミング言語', 'python', 6, true, NOW(), NOW()),
('Git', 'git', 'バージョン管理とチーム開発', 'git', 7, true, NOW(), NOW()),
('Linux コマンド', 'linux', '基本的なターミナル操作', 'terminal', 8, true, NOW(), NOW()),
('データベース', 'database', 'SQLとデータベース管理', 'database', 9, true, NOW(), NOW())
ON CONFLICT (slug) DO NOTHING;

-- 難易度挿入
INSERT INTO quiz_difficultylevel (name, slug, level, description, point_multiplier, time_limit, created_at, updated_at)
VALUES 
('初級', 'beginner', 1, '基本的な知識を問う問題', 1, 300, NOW(), NOW()),
('中級', 'intermediate', 2, '応用的な知識を問う問題', 2, 600, NOW(), NOW()),
('上級', 'advanced', 3, '高度な知識と応用力を問う問題', 3, 900, NOW(), NOW())
ON CONFLICT (slug) DO NOTHING;

-- HTML & CSSクイズ作成
INSERT INTO quiz_quiz (category_id, difficulty_id, title, description, time_limit, pass_score, is_active, thumbnail_url, banner_image_url, media_type, created_at, updated_at) VALUES
-- 初級クイズ
(1, 1, 'HTML & CSS 基礎', 'HTMLとCSSの基本的なタグとプロパティについて学びましょう', 300, 70, true, '', '', 'none', NOW(), NOW()),
-- 中級クイズ  
(1, 2, 'HTML & CSS レイアウト', 'FlexboxやGridを使ったレイアウト技法とレスポンシブデザインについて学びましょう', 600, 70, true, '', '', 'none', NOW(), NOW()),
-- 上級クイズ
(1, 3, 'HTML & CSS 応用', 'CSS詳細プロパティとアニメーション、複雑なレイアウト技法について学びましょう', 900, 70, true, '', '', 'none', NOW(), NOW())
ON CONFLICT DO NOTHING;

-- Rubyクイズ作成
INSERT INTO quiz_quiz (category_id, difficulty_id, title, description, time_limit, pass_score, is_active, thumbnail_url, banner_image_url, media_type, created_at, updated_at) VALUES
-- 初級クイズ
(2, 1, 'Ruby 基礎', 'Rubyの基本的な構文とデータ型について学びましょう', 300, 70, true, 'https://placehold.co/300x200?text=Ruby+Beginner', 'https://placehold.co/600x200?text=Ruby+Banner', 'image', NOW(), NOW()),
-- 中級クイズ
(2, 2, 'Ruby 中級', 'Enumerableや例外処理、シンボルなど中級レベルの機能を学びましょう', 600, 70, true, 'https://placehold.co/300x200?text=Ruby+Intermediate', 'https://placehold.co/600x200?text=Ruby+Banner', 'image', NOW(), NOW()),
-- 上級クイズ
(2, 3, 'Ruby 応用', 'メタプログラミングや高度な言語機能に挑戦しましょう', 900, 70, true, 'https://placehold.co/300x200?text=Ruby+Advanced', 'https://placehold.co/600x200?text=Ruby+Banner', 'image', NOW(), NOW())
ON CONFLICT DO NOTHING;

-- =========================================================
-- 4. HTML & CSS クイズ問題作成（初級）
-- =========================================================

-- 初級クイズの問題1: HTMLの基本構造
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 AND title = 'HTML & CSS 基礎'), 
'HTMLドキュメントの基本構造で、ページのタイトルを設定するために使用するタグはどれですか？', 
'multiple_choice', 
'ブラウザのタブに表示される内容を設定するタグです', 
'<title>タグはHTMLドキュメントのタイトルを設定し、ブラウザのタブやブックマークに表示されます。<head>セクション内に記述します。', 
1, 1, NOW());

-- 初級問題1の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 AND title = 'HTML & CSS 基礎') AND display_order = 1),
'<title>', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 AND title = 'HTML & CSS 基礎') AND display_order = 1),
'<header>', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 AND title = 'HTML & CSS 基礎') AND display_order = 1),
'<h1>', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 AND title = 'HTML & CSS 基礎') AND display_order = 1),
'<meta>', false, NOW(), 4);

-- =========================================================
-- 5. トリガー関数
-- =========================================================

-- updated_at 更新用関数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- ユーザー統計を更新する関数
CREATE OR REPLACE FUNCTION update_user_statistics_on_quiz_result()
RETURNS TRIGGER AS $$
DECLARE
    category_id_val INTEGER;
    difficulty_id_val INTEGER;
BEGIN
    -- クイズからカテゴリと難易度を取得
    SELECT category_id, difficulty_id INTO category_id_val, difficulty_id_val
    FROM quiz_quiz WHERE id = NEW.quiz_id;

    -- 統計テーブルが存在しない場合は作成
    INSERT INTO quiz_userstatistics (user_id, total_quizzes_completed, total_questions_answered, total_correct_answers, average_score)
    VALUES (NEW.user_id, 0, 0, 0, 0.00)
    ON CONFLICT (user_id) DO NOTHING;

    -- 統計情報を更新
    UPDATE quiz_userstatistics 
    SET 
        total_quizzes_completed = total_quizzes_completed + 1,
        total_questions_answered = total_questions_answered + NEW.total_questions,
        total_correct_answers = total_correct_answers + NEW.score,
        average_score = ROUND(
            ((total_correct_answers + NEW.score)::DECIMAL / (total_questions_answered + NEW.total_questions)) * 100, 2
        ),
        updated_at = NOW()
    WHERE user_id = NEW.user_id;

    -- 活動履歴に追加
    INSERT INTO quiz_activityhistory (user_id, quiz_id, score, completed_at, created_at)
    VALUES (NEW.user_id, NEW.quiz_id, NEW.score, NEW.completed_at, NOW());

    RETURN NEW;
END;
$$ language 'plpgsql';

-- =========================================================
-- 6. トリガー設定
-- =========================================================

-- updated_atトリガー
DROP TRIGGER IF EXISTS update_quiz_category_updated_at ON quiz_category;
CREATE TRIGGER update_quiz_category_updated_at BEFORE UPDATE ON quiz_category FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_quiz_difficultylevel_updated_at ON quiz_difficultylevel;
CREATE TRIGGER update_quiz_difficultylevel_updated_at BEFORE UPDATE ON quiz_difficultylevel FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_quiz_quiz_updated_at ON quiz_quiz;
CREATE TRIGGER update_quiz_quiz_updated_at BEFORE UPDATE ON quiz_quiz FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_quiz_quizresult_updated_at ON quiz_quizresult;
CREATE TRIGGER update_quiz_quizresult_updated_at BEFORE UPDATE ON quiz_quizresult FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_quiz_userstatistics_updated_at ON quiz_userstatistics;
CREATE TRIGGER update_quiz_userstatistics_updated_at BEFORE UPDATE ON quiz_userstatistics FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- 統計情報更新トリガー
DROP TRIGGER IF EXISTS update_statistics_on_quiz_result ON quiz_quizresult;
CREATE TRIGGER update_statistics_on_quiz_result AFTER INSERT ON quiz_quizresult FOR EACH ROW EXECUTE FUNCTION update_user_statistics_on_quiz_result();

COMMIT;

-- 結果確認用クエリ
SELECT '✅ マイグレーション完了' as status;
SELECT 'カテゴリ数: ' || COUNT(*) as categories FROM quiz_category;
SELECT '難易度数: ' || COUNT(*) as difficulties FROM quiz_difficultylevel;
SELECT 'クイズ数: ' || COUNT(*) as quizzes FROM quiz_quiz; 