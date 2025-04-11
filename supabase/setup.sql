-- Techquiz初期セットアップスクリプト
-- このスクリプトはSupabaseローカル開発環境の初期化に使用します

-- 既存のテーブルを削除（存在する場合）
DROP TABLE IF EXISTS activity_history;
DROP TABLE IF EXISTS user_statistics;
DROP TABLE IF EXISTS quiz_result;
DROP TABLE IF EXISTS answer;
DROP TABLE IF EXISTS question;
DROP TABLE IF EXISTS quiz;
DROP TABLE IF EXISTS difficulty_level;
DROP TABLE IF EXISTS category;
-- auth.usersテーブルはSupabaseによって自動的に管理されるため削除しません

-- カテゴリテーブル
CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(255),
    display_order INTEGER NOT NULL DEFAULT 0,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 難易度テーブル
CREATE TABLE difficulty_level (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    point_multiplier INTEGER NOT NULL DEFAULT 1,
    time_limit INTEGER, -- 秒単位
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- クイズテーブル
CREATE TABLE quiz (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES category(id) ON DELETE CASCADE,
    difficulty_id INTEGER REFERENCES difficulty_level(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    time_limit INTEGER, -- 秒単位
    pass_score INTEGER,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    thumbnail_url VARCHAR(255),
    banner_image_url VARCHAR(255),
    media_type VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 問題テーブル
CREATE TABLE question (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER REFERENCES quiz(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL, -- 'multiple_choice', 'text_input'など
    hint TEXT,
    explanation TEXT,
    points INTEGER NOT NULL DEFAULT 1,
    display_order INTEGER NOT NULL DEFAULT 0,
    code_snippet TEXT,
    image_url VARCHAR(255),
    media_type VARCHAR(50), -- 'code', 'image', 'diagram'など
    syntax_highlight VARCHAR(50), -- コードスニペットのシンタックスハイライト言語
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 回答選択肢テーブル
CREATE TABLE answer (
    id SERIAL PRIMARY KEY,
    question_id INTEGER REFERENCES question(id) ON DELETE CASCADE,
    answer_text TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL DEFAULT FALSE,
    feedback TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- クイズ結果テーブル
CREATE TABLE quiz_result (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    quiz_id INTEGER REFERENCES quiz(id) ON DELETE CASCADE,
    score INTEGER NOT NULL,
    total_possible INTEGER NOT NULL,
    percentage FLOAT NOT NULL,
    time_taken INTEGER, -- 秒単位
    passed BOOLEAN NOT NULL DEFAULT FALSE,
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ユーザー統計情報テーブル
CREATE TABLE user_statistics (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    category_id INTEGER REFERENCES category(id) ON DELETE SET NULL,
    difficulty_id INTEGER REFERENCES difficulty_level(id) ON DELETE SET NULL,
    quizzes_completed INTEGER NOT NULL DEFAULT 0,
    total_points INTEGER NOT NULL DEFAULT 0,
    avg_score FLOAT NOT NULL DEFAULT 0,
    highest_score INTEGER NOT NULL DEFAULT 0,
    last_quiz_date TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE (user_id, category_id, difficulty_id)
);

-- 活動履歴テーブル
CREATE TABLE activity_history (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    quiz_id INTEGER REFERENCES quiz(id) ON DELETE SET NULL,
    category_id INTEGER REFERENCES category(id) ON DELETE SET NULL,
    difficulty_id INTEGER REFERENCES difficulty_level(id) ON DELETE SET NULL,
    score INTEGER,
    percentage FLOAT,
    activity_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    activity_type VARCHAR(50) NOT NULL -- 'quiz_completion', 'review'など
);

-- Row Level Security(RLS)の設定
-- 基本的なポリシー：ユーザーは自分のデータのみアクセス可能

-- クイズ結果のRLS
ALTER TABLE quiz_result ENABLE ROW LEVEL SECURITY;
CREATE POLICY quiz_result_user_policy ON quiz_result
    USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());

-- ユーザー統計情報のRLS
ALTER TABLE user_statistics ENABLE ROW LEVEL SECURITY;
CREATE POLICY user_statistics_user_policy ON user_statistics
    USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());

-- 活動履歴のRLS
ALTER TABLE activity_history ENABLE ROW LEVEL SECURITY;
CREATE POLICY activity_history_user_policy ON activity_history
    USING (user_id = auth.uid())
    WITH CHECK (user_id = auth.uid());

-- サンプルデータの挿入

-- カテゴリのサンプルデータ
INSERT INTO category (name, description, icon, display_order) VALUES
('HTML/CSS', 'HTMLとCSSの基本的な知識を問うクイズです', 'html', 1),
('JavaScript', 'JavaScriptの基本から応用までのクイズです', 'javascript', 2),
('Git', 'Gitのコマンドと概念に関するクイズです', 'git', 3),
('Python', 'Pythonプログラミングの基礎知識を問うクイズです', 'python', 4),
('Linuxコマンド', 'Linux基本コマンドの知識を確認するクイズです', 'terminal', 5);

-- 難易度のサンプルデータ
INSERT INTO difficulty_level (name, description, point_multiplier, time_limit) VALUES
('初級', '基本的な知識を問う問題です', 1, 300),
('中級', '応用的な知識を問う問題です', 2, 600),
('上級', '高度な知識と応用力を問う問題です', 3, 900);

-- インデックスの作成（パフォーマンス向上のため）
CREATE INDEX idx_quiz_category ON quiz(category_id);
CREATE INDEX idx_quiz_difficulty ON quiz(difficulty_id);
CREATE INDEX idx_question_quiz ON question(quiz_id);
CREATE INDEX idx_answer_question ON answer(question_id);
CREATE INDEX idx_quiz_result_user ON quiz_result(user_id);
CREATE INDEX idx_quiz_result_quiz ON quiz_result(quiz_id);
CREATE INDEX idx_user_statistics_user ON user_statistics(user_id);
CREATE INDEX idx_activity_history_user ON activity_history(user_id);
CREATE INDEX idx_activity_history_date ON activity_history(activity_date);

-- 自動更新関数と関連するトリガー

-- quiz更新時のupdated_at更新
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_quiz_updated_at
    BEFORE UPDATE ON quiz
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_statistics_updated_at
    BEFORE UPDATE ON user_statistics
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
    FROM quiz WHERE id = NEW.quiz_id;
    
    -- 全体統計の更新または挿入（カテゴリ、難易度なし）
    INSERT INTO user_statistics (
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
        quizzes_completed = user_statistics.quizzes_completed + 1,
        total_points = user_statistics.total_points + NEW.score,
        avg_score = (user_statistics.avg_score * user_statistics.quizzes_completed + NEW.percentage) / (user_statistics.quizzes_completed + 1),
        highest_score = GREATEST(user_statistics.highest_score, NEW.score),
        last_quiz_date = NEW.completed_at,
        updated_at = NOW();
    
    -- カテゴリ別統計の更新または挿入
    IF category_id_val IS NOT NULL THEN
        INSERT INTO user_statistics (
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
            quizzes_completed = user_statistics.quizzes_completed + 1,
            total_points = user_statistics.total_points + NEW.score,
            avg_score = (user_statistics.avg_score * user_statistics.quizzes_completed + NEW.percentage) / (user_statistics.quizzes_completed + 1),
            highest_score = GREATEST(user_statistics.highest_score, NEW.score),
            last_quiz_date = NEW.completed_at,
            updated_at = NOW();
    END IF;
    
    -- 難易度別統計の更新または挿入
    IF difficulty_id_val IS NOT NULL THEN
        INSERT INTO user_statistics (
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
            quizzes_completed = user_statistics.quizzes_completed + 1,
            total_points = user_statistics.total_points + NEW.score,
            avg_score = (user_statistics.avg_score * user_statistics.quizzes_completed + NEW.percentage) / (user_statistics.quizzes_completed + 1),
            highest_score = GREATEST(user_statistics.highest_score, NEW.score),
            last_quiz_date = NEW.completed_at,
            updated_at = NOW();
    END IF;
    
    -- カテゴリ・難易度別統計の更新または挿入
    IF category_id_val IS NOT NULL AND difficulty_id_val IS NOT NULL THEN
        INSERT INTO user_statistics (
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
            quizzes_completed = user_statistics.quizzes_completed + 1,
            total_points = user_statistics.total_points + NEW.score,
            avg_score = (user_statistics.avg_score * user_statistics.quizzes_completed + NEW.percentage) / (user_statistics.quizzes_completed + 1),
            highest_score = GREATEST(user_statistics.highest_score, NEW.score),
            last_quiz_date = NEW.completed_at,
            updated_at = NOW();
    END IF;
    
    -- 活動履歴に記録
    INSERT INTO activity_history (
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
        'quiz_completion'
    );
    
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER trigger_update_user_statistics
    AFTER INSERT ON quiz_result
    FOR EACH ROW
    EXECUTE FUNCTION update_user_statistics_on_quiz_result();

-- 古い活動履歴を自動アーカイブするためのメンテナンス関数（cron jobから呼び出し可能）
CREATE OR REPLACE FUNCTION archive_old_activity_history(days_to_keep INTEGER DEFAULT 90)
RETURNS INTEGER AS $$
DECLARE
    archive_date TIMESTAMP WITH TIME ZONE;
    deleted_count INTEGER;
BEGIN
    archive_date := NOW() - (days_to_keep * INTERVAL '1 day');
    
    -- 古い記録を削除（実際のアプリケーションでは別のアーカイブテーブルに移動することも検討）
    DELETE FROM activity_history 
    WHERE activity_date < archive_date
    RETURNING COUNT(*) INTO deleted_count;
    
    RETURN deleted_count;
END;
$$ language 'plpgsql';

-- コメント
COMMENT ON TABLE category IS 'クイズのカテゴリ（言語や技術など）';
COMMENT ON TABLE difficulty_level IS 'クイズの難易度レベル（初級、中級、上級など）';
COMMENT ON TABLE quiz IS 'クイズの基本情報';
COMMENT ON TABLE question IS 'クイズに含まれる問題';
COMMENT ON TABLE answer IS '問題の選択肢や回答';
COMMENT ON TABLE quiz_result IS 'ユーザーのクイズ結果';
COMMENT ON TABLE user_statistics IS 'ユーザーの学習統計情報';
COMMENT ON TABLE activity_history IS 'ユーザーの学習活動履歴'; 