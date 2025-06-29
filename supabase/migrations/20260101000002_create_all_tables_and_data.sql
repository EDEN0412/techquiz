-- 全テーブル作成と初期データ投入マイグレーション
-- 作成日: 2025-01-18

BEGIN;

-- =========================================================
-- 0. 既存テーブルの削除（冪等性確保のため）
-- =========================================================
-- Djangoが管理するテーブルは削除しない（auth_*, django_*, token_blacklist_*）
DROP TABLE IF EXISTS quiz_activityhistory CASCADE;
DROP TABLE IF EXISTS quiz_userstatistics CASCADE;
DROP TABLE IF EXISTS quiz_quizresult CASCADE;
DROP TABLE IF EXISTS quiz_answer CASCADE;
DROP TABLE IF EXISTS quiz_question CASCADE;
DROP TABLE IF EXISTS quiz_quiz CASCADE;
DROP TABLE IF EXISTS quiz_difficultylevel CASCADE;
DROP TABLE IF EXISTS quiz_category CASCADE;

-- =========================================================
-- 1. テーブル作成
-- =========================================================

-- Django管理テーブル（auth_*, django_*, token_blacklist_*）はDjangoマイグレーションで作成

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

-- JWT トークンブラックリスト関連テーブルはDjangoマイグレーションで作成

-- =========================================================
-- 2. インデックス作成
-- =========================================================

-- クイズ関連テーブルのインデックス作成
CREATE INDEX quiz_quiz_category_id_idx ON quiz_quiz(category_id);
CREATE INDEX quiz_quiz_difficulty_id_idx ON quiz_quiz(difficulty_id);
CREATE INDEX quiz_question_quiz_id_idx ON quiz_question(quiz_id);
CREATE INDEX quiz_answer_question_id_idx ON quiz_answer(question_id);
CREATE INDEX quiz_quizresult_user_id_idx ON quiz_quizresult(user_id);
CREATE INDEX quiz_quizresult_quiz_id_idx ON quiz_quizresult(quiz_id);
CREATE INDEX quiz_activityhistory_user_id_idx ON quiz_activityhistory(user_id);

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

-- =========================================================
-- 4. HTML & CSS クイズ問題作成（全難易度）
-- =========================================================

-- HTML & CSS 初級問題（全5問）
-- 問題1: HTMLの基本構造
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 AND title = 'HTML & CSS 基礎'), 
'HTMLドキュメントの基本構造で、ページのタイトルを設定するために使用するタグはどれですか？', 
'multiple_choice', 
'ブラウザのタブに表示される内容を設定するタグです', 
'<title>タグはHTMLドキュメントのタイトルを設定し、ブラウザのタブやブックマークに表示されます。<head>セクション内に記述します。', 
1, 1, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 AND title = 'HTML & CSS 基礎') AND display_order = 1),
'<title>', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 AND title = 'HTML & CSS 基礎') AND display_order = 1),
'<header>', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 AND title = 'HTML & CSS 基礎') AND display_order = 1),
'<h1>', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 AND title = 'HTML & CSS 基礎') AND display_order = 1),
'<meta>', false, NOW(), 4);

-- 問題2: CSSの基本
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1), 
'CSSでテキストの色を赤色に設定するプロパティと値の正しい組み合わせはどれですか？', 
'multiple_choice', 
'色を指定するCSSプロパティを考えてみましょう', 
'color プロパティは要素のテキスト色を設定します。red は基本的な色名の一つで、#ff0000 や rgb(255,0,0) でも同じ赤色を表現できます。', 
1, 2, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 2),
'color: red;', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 2),
'text-color: red;', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 2),
'background: red;', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 2),
'font-color: red;', false, NOW(), 4);

-- 問題3: HTMLのリスト
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1), 
'HTMLで番号付きリスト（順序付きリスト）を作成するために使用するタグはどれですか？', 
'multiple_choice', 
'数字が自動的に付与されるリストのタグです', 
'<ol>（Ordered List）は番号付きリストを作成します。<ul>は番号なしリスト、<li>は各リスト項目を表します。', 
1, 3, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 3),
'<ol>', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 3),
'<ul>', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 3),
'<list>', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 3),
'<li>', false, NOW(), 4);

-- 問題4: CSSセレクタ
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1), 
'CSSでクラス名「menu」が付いた要素を選択するセレクタはどれですか？', 
'multiple_choice', 
'クラスセレクタは特定の記号から始まります', 
'クラスセレクタは「.」（ドット）で始まります。.menu は class="menu" が指定された全ての要素を選択します。', 
1, 4, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 4),
'.menu', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 4),
'#menu', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 4),
'menu', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 4),
'@menu', false, NOW(), 4);

-- 問題5: HTMLの画像タグ
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1), 
'HTMLで画像を表示するために使用するタグはどれですか？', 
'multiple_choice', 
'Image（画像）の略称がタグ名になっています', 
'<img>タグは画像を表示するために使用します。src属性で画像ファイルのパスを指定し、alt属性で代替テキストを設定します。', 
1, 5, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 5),
'<img>', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 5),
'<image>', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 5),
'<pic>', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 5),
'<photo>', false, NOW(), 4);

-- =========================================================
-- HTML & CSS 中級問題（全5問）
-- =========================================================

-- 問題1: Flexbox
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2), 
'CSSのFlexboxで、アイテムを横方向（主軸）に中央揃えするプロパティと値はどれですか？', 
'multiple_choice', 
'justify-content プロパティの値を考えてみましょう', 
'justify-content: center; は Flexbox の主軸（通常は横方向）でアイテムを中央揃えします。align-items は交差軸の配置を制御します。', 
2, 1, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 1),
'justify-content: center;', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 1),
'align-items: center;', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 1),
'text-align: center;', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 1),
'flex-align: center;', false, NOW(), 4);

-- 問題2: CSS Grid
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2), 
'CSS Gridで3列のグリッドレイアウトを作成するプロパティと値はどれですか？', 
'multiple_choice', 
'グリッドのテンプレート列を定義するプロパティです', 
'grid-template-columns: 1fr 1fr 1fr; または repeat(3, 1fr) で3列の等幅グリッドを作成できます。1frは利用可能なスペースの1分割を表します。', 
2, 2, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 2),
'grid-template-columns: 1fr 1fr 1fr;', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 2),
'grid-columns: 3;', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 2),
'column-count: 3;', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 2),
'flex-columns: 3;', false, NOW(), 4);

-- 問題3: レスポンシブデザイン
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2), 
'CSSのメディアクエリで、画面幅が768px以下の場合にスタイルを適用するための正しい記述はどれですか？', 
'multiple_choice', 
'max-width を使って最大幅を指定します', 
'@media (max-width: 768px) はビューポートの幅が768px以下の場合にスタイルを適用します。レスポンシブデザインの基本的な記述方法です。', 
2, 3, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 3),
'@media (max-width: 768px)', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 3),
'@media (width <= 768px)', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 3),
'@responsive (max-width: 768px)', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 3),
'@screen (width: 768px)', false, NOW(), 4);

-- 問題4: CSS擬似クラス
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2), 
'リンクにマウスを乗せたときのスタイルを指定するCSS擬似クラスはどれですか？', 
'multiple_choice', 
'マウスを「乗せる」という動作に対応する擬似クラスです', 
':hover 擬似クラスはマウスカーソルが要素上にある間のスタイルを指定します。インタラクティブなUI作成に重要な要素です。', 
2, 4, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 4),
':hover', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 4),
':focus', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 4),
':active', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 4),
':visited', false, NOW(), 4);

-- 問題5: positionプロパティ  
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2), 
'CSSのpositionプロパティで、スクロールしても常に画面の同じ位置に固定表示するための値はどれですか？', 
'multiple_choice', 
'「固定」を意味する英単語がヒントです', 
'position: fixed; は要素をビューポートに対して固定位置に配置します。スクロールしても位置が変わらず、ヘッダーやフローティングボタンなどによく使用されます。', 
2, 5, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 5),
'fixed', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 5),
'absolute', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 5),
'relative', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 5),
'static', false, NOW(), 4);

-- =========================================================
-- 5. Ruby クイズ問題作成（全難易度）
-- =========================================================

-- Ruby 初級問題（全5問）
-- 問題1: puts
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1),
'Rubyでコンソールに文字列を改行付きで出力するメソッドはどれですか？','multiple_choice','標準出力に文字列を書き込み、末尾に改行を追加します','puts メソッドは与えられた文字列を改行付きで出力します。',1,1,NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=1),'puts',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=1),'print',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=1),'echo',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=1),'console.log',false,NOW(),4);

-- 問題2: nil
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1),
'Rubyで「値が存在しない」ことを表すオブジェクトはどれですか？','multiple_choice','他言語の null に相当します','nil は Ruby で「何もない」ことを示す唯一のオブジェクトです。',1,2,NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=2),'nil',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=2),'null',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=2),'None',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=2),'undefined',false,NOW(),4);

-- 問題3: push
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1),
'Rubyで配列の末尾に要素を追加するメソッドはどれですか？','multiple_choice','<< 演算子のエイリアスです','push メソッド（または << 演算子）を使って配列末尾に要素を追加します。',1,3,NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=3),'push',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=3),'add',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=3),'append',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=3),'insert',false,NOW(),4);

-- 問題4: 文字列連結
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1),
'Rubyで文字列を連結する演算子はどれですか？','multiple_choice','足し算と同じ記号です','Ruby では + 演算子で文字列連結ができます。',1,4,NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=4),'+',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=4),'&',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=4),'.',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=4),'=>',false,NOW(),4);

-- 問題5: pop
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1),
'Rubyで配列の最後の要素を取り出して削除するメソッドはどれですか？','multiple_choice','shift は先頭要素を返します','pop メソッドで末尾要素を返して削除できます。',1,5,NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=5),'pop',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=5),'delete',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=5),'remove_last',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=5),'slice!',false,NOW(),4);

-- =========================================================
-- Ruby 中級問題（全5問）
-- =========================================================

-- 問題1: map メソッドの戻り値
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2),
'Enumerable#map メソッドを呼び出したときの戻り値として正しいものはどれですか？',
'multiple_choice',
'変換結果を保持します',
'map はブロックの戻り値を要素として持つ「新しい配列」を返します。元の配列は変化しません。',
2,1,NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2) AND display_order=1),'ブロック結果を要素とする新しい配列',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2) AND display_order=1),'nil',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2) AND display_order=1),'self と同じ配列',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2) AND display_order=1),'Enumerator オブジェクト',false,NOW(),4);

-- 問題2: &: 記法
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2),
'Array#map(&:to_s) の &: 記法が内部で実行している処理はどれですか？',
'multiple_choice',
'Proc オブジェクトに変換します',
'&:symbol は Symbol#to_proc を呼び出してブロックに変換し、要素に対してメソッド呼び出しを行います。',
2,2,NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2) AND display_order=2),'Symbol#to_proc でブロックを生成して呼び出す',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2) AND display_order=2),'each に書き換えて実行',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2) AND display_order=2),'メタプログラミングでメソッドを定義',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2) AND display_order=2),'特別な構文糖で RubyVM が最適化',false,NOW(),4);

-- 問題3: 例外処理の継承順
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2),
'rescue 節で複数の例外クラスを書く場合、評価順として正しいのはどれですか？',
'multiple_choice',
'より具体的な例外から書きます',
'上位クラスを先に書くと下位クラスに到達せず捕捉されないため、具体的（サブクラス）→一般的（スーパークラス）の順に記述します。',
2,3,NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2) AND display_order=3),'サブクラスを先、スーパークラスを後',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2) AND display_order=3),'スーパークラスを先、サブクラスを後',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2) AND display_order=3),'アルファベット順',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2) AND display_order=3),'記述順は影響しない',false,NOW(),4);

-- 問題4: attr_accessor
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2),
'`attr_accessor :name` をクラスに定義すると生成されるメソッドの組み合わせはどれですか？',
'multiple_choice',
'読み取りと書き込み',
'attr_accessor は同名のゲッターとセッターを定義します。インスタンス変数 @name に対するアクセスを簡略化します。',
2,4,NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2) AND display_order=4),'name と name=',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2) AND display_order=4),'get_name と set_name',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2) AND display_order=4),'initialize と to_s',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2) AND display_order=4),'name? と name!',false,NOW(),4);

-- 問題5: include と extend
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2),
'Module を mixin する際、インスタンスメソッドとして追加するキーワードはどれですか？',
'multiple_choice',
'クラスに「混ぜる」イメージ',
'include はモジュールのメソッドをインスタンスメソッドとして、extend はクラスメソッドとして追加します。',
2,5,NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2) AND display_order=5),'include',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2) AND display_order=5),'extend',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2) AND display_order=5),'prepend',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2) AND display_order=5),'require',false,NOW(),4);

-- =========================================================
-- Ruby 上級問題（全5問）
-- =========================================================

-- 問題1: method_missing
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3),
'クラスで `def method_missing(name, *args); end` をオーバーライドしたとき、暗黙で **呼び出されなくなる** メソッドフックはどれですか？',
'multiple_choice',
'無限再帰を避けるために分かれています',
'respond_to_missing? は method_missing と対になるフックで、メソッド応答判定に使われます。method_missing を定義しても respond_to_missing? が自動定義されることはありません。',
3,1,NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3) AND display_order=1),'respond_to_missing?',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3) AND display_order=1),'initialize_copy',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3) AND display_order=1),'method_added',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3) AND display_order=1),'included',false,NOW(),4);

-- 問題2: eigenclass
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3),
'次のコードで `self` が指すオブジェクトは何ですか？\n```ruby\nobj = "hello"\nclass << obj\n  self\nend\n```',
'multiple_choice',
'単独の特異クラス',
'`class << obj` は obj の特異クラス（eigenclass）をオープンします。よって self はその特異クラスを指します。',
3,2,NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3) AND display_order=2),'obj の特異クラス',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3) AND display_order=2),'String クラス',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3) AND display_order=2),'obj 自身 ("hello")',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3) AND display_order=2),'main オブジェクト',false,NOW(),4);

-- 問題3: refine
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3),
'Ruby の Refinements 機能を有効化するキーワードはどれですか？',
'multiple_choice',
'using 〇〇',
'Refinements を有効にするには `using モジュール名` をソースのトップレベルかクラス/モジュール定義内で呼び出します。',
3,3,NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3) AND display_order=3),'using',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3) AND display_order=3),'import',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3) AND display_order=3),'include',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3) AND display_order=3),'extend',false,NOW(),4);

-- 問題4: Fiber#resume の戻り値
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3),
'Fiber#resume を呼び出したとき、呼び出し側に返る値として正しいものはどれですか？',
'multiple_choice',
'yield と同様のイメージ',
'Fiber#resume は Fiber 内で `yield`（または最終値）によって外に渡されたオブジェクトを返します。',
3,4,NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3) AND display_order=4),'Fiber 内から yield された値',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3) AND display_order=4),'nil 固定',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3) AND display_order=4),'Fiber オブジェクト自身',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3) AND display_order=4),'次に resume で渡す引数',false,NOW(),4);

-- 問題5: prepend
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3),
'Module#prepend を使ってモジュールをミックスインした場合のメソッド探索順として正しいものはどれですか？',
'multiple_choice',
'prepend は「先頭に挿入」',
'prepend はモジュールをクラスの祖先チェーンの先頭に挿入するため、そのモジュールのメソッドがクラスの同名メソッドより優先します。',
3,5,NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3) AND display_order=5),'モジュール → クラス → 既存の祖先',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3) AND display_order=5),'クラス → モジュール → 既存の祖先',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3) AND display_order=5),'既存の祖先 → クラス → モジュール',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3) AND display_order=5),'モジュールは探索に含まれない',false,NOW(),4);

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