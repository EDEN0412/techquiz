-- Techquiz初期セットアップスクリプト（Djangoモデル対応版）
-- このスクリプトはSupabaseローカル開発環境の初期化に使用します

-- 既存のテーブルを削除（存在する場合）
DROP TABLE IF EXISTS quiz_activityhistory;
DROP TABLE IF EXISTS quiz_userstatistics;
DROP TABLE IF EXISTS quiz_quizresult;
DROP TABLE IF EXISTS quiz_answer;
DROP TABLE IF EXISTS quiz_question;
DROP TABLE IF EXISTS quiz_quiz;
DROP TABLE IF EXISTS quiz_difficultylevel;
DROP TABLE IF EXISTS quiz_category;
DROP TABLE IF EXISTS auth_user;
-- auth.usersテーブルはSupabaseによって自動的に管理されるため削除しません

-- Django標準のユーザーテーブル（auth.User）
CREATE TABLE auth_user (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    username VARCHAR(150) NOT NULL UNIQUE,
    email VARCHAR(254) NOT NULL DEFAULT '',
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- auth_userテーブルのインデックス
CREATE INDEX auth_user_username_idx ON auth_user(username);
CREATE INDEX auth_user_email_idx ON auth_user(email);

-- カテゴリテーブル（Djangoモデル: quiz.Category）
CREATE TABLE quiz_category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    icon VARCHAR(50),
    display_order INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 難易度テーブル（Djangoモデル: quiz.DifficultyLevel）
CREATE TABLE quiz_difficultylevel (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    slug VARCHAR(50) NOT NULL UNIQUE,
    level INTEGER NOT NULL UNIQUE,
    description TEXT,
    point_multiplier INTEGER NOT NULL DEFAULT 1,
    time_limit INTEGER NOT NULL DEFAULT 600, -- 秒単位
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- クイズテーブル（Djangoモデル: quiz.Quiz）
CREATE TABLE quiz_quiz (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES quiz_category(id) ON DELETE CASCADE,
    difficulty_id INTEGER REFERENCES quiz_difficultylevel(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    time_limit INTEGER, -- 秒単位
    pass_score INTEGER,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 問題テーブル（Djangoモデル: quiz.Question）
CREATE TABLE quiz_question (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER REFERENCES quiz_quiz(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL DEFAULT 'multiple_choice',
    hint TEXT,
    explanation TEXT,
    points INTEGER NOT NULL DEFAULT 1,
    "order" INTEGER NOT NULL DEFAULT 0, -- orderは予約語のため""で囲む
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 回答選択肢テーブル（Djangoモデル: quiz.Answer）
CREATE TABLE quiz_answer (
    id SERIAL PRIMARY KEY,
    question_id INTEGER REFERENCES quiz_question(id) ON DELETE CASCADE,
    answer_text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL DEFAULT FALSE,
    "order" INTEGER NOT NULL DEFAULT 0, -- orderは予約語のため""で囲む
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- クイズ結果テーブル（Djangoモデル: quiz.QuizResult）
CREATE TABLE quiz_quizresult (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES auth_user(id) ON DELETE CASCADE,
    quiz_id INTEGER REFERENCES quiz_quiz(id) ON DELETE CASCADE,
    score INTEGER NOT NULL,
    total_possible INTEGER NOT NULL,
    percentage FLOAT NOT NULL,
    time_taken INTEGER, -- 秒単位
    passed BOOLEAN NOT NULL DEFAULT FALSE,
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ユーザー統計情報テーブル（Djangoモデル: quiz.UserStatistics）
CREATE TABLE quiz_userstatistics (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES auth_user(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES quiz_category(id) ON DELETE SET NULL,
    difficulty_id INTEGER REFERENCES quiz_difficultylevel(id) ON DELETE SET NULL,
    quizzes_completed INTEGER NOT NULL DEFAULT 0,
    total_points INTEGER NOT NULL DEFAULT 0,
    avg_score FLOAT NOT NULL DEFAULT 0,
    highest_score INTEGER NOT NULL DEFAULT 0,
    last_quiz_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE (user_id, category_id, difficulty_id)
);

-- 活動履歴テーブル（Djangoモデル: quiz.ActivityHistory）
CREATE TABLE quiz_activityhistory (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES auth_user(id) ON DELETE CASCADE,
    quiz_id INTEGER REFERENCES quiz_quiz(id) ON DELETE SET NULL,
    category_id INTEGER REFERENCES quiz_category(id) ON DELETE SET NULL,
    difficulty_id INTEGER REFERENCES quiz_difficultylevel(id) ON DELETE SET NULL,
    score INTEGER,
    percentage FLOAT,
    activity_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    activity_type VARCHAR(50) NOT NULL DEFAULT 'quiz_completed',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Row Level Security(RLS)の設定
-- 基本的なポリシー：ユーザーは自分のデータのみアクセス可能

-- Row Level Security(RLS)の設定
-- 注意: Django認証を使用する場合、RLSはアプリケーションレベルで制御することが一般的
-- 以下のRLSポリシーは参考用として残しますが、実際の運用ではDjangoのPermissionシステムを使用

-- クイズ結果のRLS（Django認証用）
ALTER TABLE quiz_quizresult ENABLE ROW LEVEL SECURITY;
-- Django認証では、アプリケーションレベルでuser_idを検証するため、
-- ここでは基本的なポリシーのみ設定
CREATE POLICY quiz_quizresult_user_policy ON quiz_quizresult
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- ユーザー統計情報のRLS（Django認証用）
ALTER TABLE quiz_userstatistics ENABLE ROW LEVEL SECURITY;
CREATE POLICY quiz_userstatistics_user_policy ON quiz_userstatistics
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- 活動履歴のRLS（Django認証用）
ALTER TABLE quiz_activityhistory ENABLE ROW LEVEL SECURITY;
CREATE POLICY quiz_activityhistory_user_policy ON quiz_activityhistory
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- サンプルデータの挿入

-- カテゴリのサンプルデータ
INSERT INTO quiz_category (name, slug, description, icon, display_order) VALUES
('HTML & CSS', 'html-css', 'Webの基礎とスタイリングを習得', 'html', 1),
('Ruby', 'ruby', 'オブジェクト指向スクリプト言語の基礎', 'ruby', 2),
('Ruby on Rails', 'ruby-rails', 'Rubyベースの高速Webアプリケーション開発', 'rails', 3),
('JavaScript', 'javascript', 'Web開発に不可欠なプログラミング言語', 'javascript', 4),
('Webアプリケーション基礎', 'web-app-basic', 'Webアプリ開発の基礎知識とアーキテクチャ', 'web', 5),
('Python', 'python', '汎用性の高い読みやすいプログラミング言語', 'python', 6),
('Git', 'git', 'バージョン管理とチーム開発', 'git', 7),
('Linux コマンド', 'linux', '基本的なターミナル操作', 'terminal', 8),
('データベース', 'database', 'SQLとデータベース管理', 'database', 9);

-- 難易度のサンプルデータ
INSERT INTO quiz_difficultylevel (name, slug, level, description, point_multiplier, time_limit) VALUES
('初級', 'beginner', 1, '基本的な知識を問う問題', 1, 300),
('中級', 'intermediate', 2, '応用的な知識を問う問題', 2, 600),
('上級', 'advanced', 3, '高度な知識と応用力を問う問題', 3, 900);

-- インデックスの作成（パフォーマンス向上のため）
CREATE INDEX idx_quiz_quiz_category ON quiz_quiz(category_id);
CREATE INDEX idx_quiz_quiz_difficulty ON quiz_quiz(difficulty_id);
CREATE INDEX idx_quiz_question_quiz ON quiz_question(quiz_id);
CREATE INDEX idx_quiz_answer_question ON quiz_answer(question_id);
CREATE INDEX idx_quiz_quizresult_user ON quiz_quizresult(user_id);
CREATE INDEX idx_quiz_quizresult_quiz ON quiz_quizresult(quiz_id);
CREATE INDEX idx_quiz_userstatistics_user ON quiz_userstatistics(user_id);
CREATE INDEX idx_quiz_activityhistory_user ON quiz_activityhistory(user_id);
CREATE INDEX idx_quiz_activityhistory_date ON quiz_activityhistory(activity_date);

-- 自動更新関数と関連するトリガー

-- updated_at更新関数
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- 各テーブルのupdated_atトリガー
CREATE TRIGGER update_quiz_category_updated_at
    BEFORE UPDATE ON quiz_category
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_quiz_difficultylevel_updated_at
    BEFORE UPDATE ON quiz_difficultylevel
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_quiz_quiz_updated_at
    BEFORE UPDATE ON quiz_quiz
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_quiz_question_updated_at
    BEFORE UPDATE ON quiz_question
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_quiz_answer_updated_at
    BEFORE UPDATE ON quiz_answer
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_quiz_quizresult_updated_at
    BEFORE UPDATE ON quiz_quizresult
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_quiz_userstatistics_updated_at
    BEFORE UPDATE ON quiz_userstatistics
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_quiz_activityhistory_updated_at
    BEFORE UPDATE ON quiz_activityhistory
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- クイズ結果登録時に自動的にユーザー統計情報を更新するトリガー
CREATE OR REPLACE FUNCTION update_user_statistics_on_quiz_result()
RETURNS TRIGGER AS $$
DECLARE
    category_id_val INTEGER;
    difficulty_id_val INTEGER;
BEGIN
    -- クイズからカテゴリIDと難易度IDを取得
    SELECT category_id, difficulty_id INTO category_id_val, difficulty_id_val
    FROM quiz_quiz WHERE id = NEW.quiz_id;
    
    -- 全体統計の更新または挿入（カテゴリ、難易度なし）
    INSERT INTO quiz_userstatistics (
        user_id, 
        quizzes_completed, 
        total_points, 
        avg_score, 
        highest_score,
        last_quiz_date
    ) VALUES (
        NEW.user_id, 
        1, 
        NEW.score, 
        NEW.percentage, 
        NEW.score,
        NEW.completed_at
    )
    ON CONFLICT (user_id, category_id, difficulty_id) 
    DO UPDATE SET
        quizzes_completed = quiz_userstatistics.quizzes_completed + 1,
        total_points = quiz_userstatistics.total_points + NEW.score,
        avg_score = (quiz_userstatistics.avg_score * quiz_userstatistics.quizzes_completed + NEW.percentage) / (quiz_userstatistics.quizzes_completed + 1),
        highest_score = GREATEST(quiz_userstatistics.highest_score, NEW.score),
        last_quiz_date = NEW.completed_at,
        updated_at = NOW();
    
    -- カテゴリ別統計の更新または挿入
    IF category_id_val IS NOT NULL THEN
        INSERT INTO quiz_userstatistics (
            user_id, 
            category_id,
            quizzes_completed, 
            total_points, 
            avg_score, 
            highest_score,
            last_quiz_date
        ) VALUES (
            NEW.user_id, 
            category_id_val,
            1, 
            NEW.score, 
            NEW.percentage, 
            NEW.score,
            NEW.completed_at
        )
        ON CONFLICT (user_id, category_id, difficulty_id) 
        DO UPDATE SET
            quizzes_completed = quiz_userstatistics.quizzes_completed + 1,
            total_points = quiz_userstatistics.total_points + NEW.score,
            avg_score = (quiz_userstatistics.avg_score * quiz_userstatistics.quizzes_completed + NEW.percentage) / (quiz_userstatistics.quizzes_completed + 1),
            highest_score = GREATEST(quiz_userstatistics.highest_score, NEW.score),
            last_quiz_date = NEW.completed_at,
            updated_at = NOW();
    END IF;
    
    -- 難易度別統計の更新または挿入
    IF difficulty_id_val IS NOT NULL THEN
        INSERT INTO quiz_userstatistics (
            user_id, 
            difficulty_id,
            quizzes_completed, 
            total_points, 
            avg_score, 
            highest_score,
            last_quiz_date
        ) VALUES (
            NEW.user_id, 
            difficulty_id_val,
            1, 
            NEW.score, 
            NEW.percentage, 
            NEW.score,
            NEW.completed_at
        )
        ON CONFLICT (user_id, category_id, difficulty_id) 
        DO UPDATE SET
            quizzes_completed = quiz_userstatistics.quizzes_completed + 1,
            total_points = quiz_userstatistics.total_points + NEW.score,
            avg_score = (quiz_userstatistics.avg_score * quiz_userstatistics.quizzes_completed + NEW.percentage) / (quiz_userstatistics.quizzes_completed + 1),
            highest_score = GREATEST(quiz_userstatistics.highest_score, NEW.score),
            last_quiz_date = NEW.completed_at,
            updated_at = NOW();
    END IF;
    
    -- カテゴリ・難易度別統計の更新または挿入
    IF category_id_val IS NOT NULL AND difficulty_id_val IS NOT NULL THEN
        INSERT INTO quiz_userstatistics (
            user_id, 
            category_id,
            difficulty_id,
            quizzes_completed, 
            total_points, 
            avg_score, 
            highest_score,
            last_quiz_date
        ) VALUES (
            NEW.user_id, 
            category_id_val,
            difficulty_id_val,
            1, 
            NEW.score, 
            NEW.percentage, 
            NEW.score,
            NEW.completed_at
        )
        ON CONFLICT (user_id, category_id, difficulty_id) 
        DO UPDATE SET
            quizzes_completed = quiz_userstatistics.quizzes_completed + 1,
            total_points = quiz_userstatistics.total_points + NEW.score,
            avg_score = (quiz_userstatistics.avg_score * quiz_userstatistics.quizzes_completed + NEW.percentage) / (quiz_userstatistics.quizzes_completed + 1),
            highest_score = GREATEST(quiz_userstatistics.highest_score, NEW.score),
            last_quiz_date = NEW.completed_at,
            updated_at = NOW();
    END IF;
    
    -- 活動履歴に記録
    INSERT INTO quiz_activityhistory (
        user_id,
        quiz_id,
        category_id,
        difficulty_id,
        score,
        percentage,
        activity_type
    ) VALUES (
        NEW.user_id,
        NEW.quiz_id,
        category_id_val,
        difficulty_id_val,
        NEW.score,
        NEW.percentage,
        'quiz_completed'
    );
    
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER trigger_update_user_statistics
    AFTER INSERT ON quiz_quizresult
    FOR EACH ROW
    EXECUTE FUNCTION update_user_statistics_on_quiz_result();

-- テーブルコメント（参考用）
COMMENT ON TABLE auth_user IS 'Django標準ユーザーテーブル（Django: django.contrib.auth.models.User）';
COMMENT ON TABLE quiz_category IS 'クイズカテゴリテーブル（Django: quiz.Category）';
COMMENT ON TABLE quiz_difficultylevel IS '難易度レベルテーブル（Django: quiz.DifficultyLevel）';
COMMENT ON TABLE quiz_quiz IS 'クイズテーブル（Django: quiz.Quiz）';
COMMENT ON TABLE quiz_question IS 'クイズ問題テーブル（Django: quiz.Question）';
COMMENT ON TABLE quiz_answer IS '回答選択肢テーブル（Django: quiz.Answer）';
COMMENT ON TABLE quiz_quizresult IS 'クイズ結果テーブル（Django: quiz.QuizResult）';
COMMENT ON TABLE quiz_userstatistics IS 'ユーザー統計情報テーブル（Django: quiz.UserStatistics）';
COMMENT ON TABLE quiz_activityhistory IS '活動履歴テーブル（Django: quiz.ActivityHistory）';

-- =========================================================
-- クイズ問題データ (HTML & CSS, 初級〜上級)
-- Supabase CLI の db reset 時に自動で取り込むため、
-- 外部 SQL ファイルを読み込みます。
-- =========================================================
\i migrations/create_html_css_quiz_part1_fixed2.sql
\i migrations/create_html_css_quiz_part2_fixed2.sql 