-- HTML & CSSクイズ問題作成スクリプト
-- カテゴリID: 1 (HTML & CSS)
-- 3つの難易度レベルそれぞれにクイズを作成

BEGIN;

-- =========================================================
-- カテゴリ挿入 (quiz_category)
-- =========================================================
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
('データベース', 'database', 'SQLとデータベース管理', 'database', 9, true, NOW(), NOW());

-- =========================================================
-- 難易度挿入 (quiz_difficultylevel)
-- ID は 1: 初級, 2: 中級, 3: 上級 になる順で投入
-- =========================================================
INSERT INTO quiz_difficultylevel (name, slug, level, description, point_multiplier, time_limit, created_at, updated_at)
VALUES 
('初級', 'beginner', 1, '基本的な知識を問う問題', 1, 300, NOW(), NOW()),
('中級', 'intermediate', 2, '応用的な知識を問う問題', 2, 600, NOW(), NOW()),
('上級', 'advanced', 3, '高度な知識と応用力を問う問題', 3, 900, NOW(), NOW());

-- 1. クイズの作成
INSERT INTO quiz_quiz (category_id, difficulty_id, title, description, time_limit, pass_score, is_active, thumbnail_url, banner_image_url, media_type, created_at, updated_at) VALUES
-- 初級クイズ
(1, 1, 'HTML & CSS 基礎', 'HTMLとCSSの基本的なタグとプロパティについて学びましょう', 300, 70, true, '', '', 'none', NOW(), NOW()),
-- 中級クイズ  
(1, 2, 'HTML & CSS レイアウト', 'FlexboxやGridを使ったレイアウト技法とレスポンシブデザインについて学びましょう', 600, 70, true, '', '', 'none', NOW(), NOW()),
-- 上級クイズ
(1, 3, 'HTML & CSS 応用', 'CSS詳細プロパティとアニメーション、複雑なレイアウト技法について学びましょう', 900, 70, true, '', '', 'none', NOW(), NOW());

-- 作成されたクイズのIDを取得するため、一旦確認
-- 初級クイズID、中級クイズID、上級クイズIDを使って問題を作成

-- 2. 初級レベルの問題作成（基本的なHTMLタグとCSS）

-- 初級クイズの問題1: HTMLの基本構造
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1), 
'HTMLドキュメントの基本構造で、ページのタイトルを設定するために使用するタグはどれですか？', 
'multiple_choice', 
'ブラウザのタブに表示される内容を設定するタグです', 
'<title>タグはHTMLドキュメントのタイトルを設定し、ブラウザのタブやブックマークに表示されます。<head>セクション内に記述します。', 
1, 1, NOW());

-- 初級問題1の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 1),
'<title>', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 1),
'<header>', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 1),
'<h1>', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 1),
'<meta>', false, NOW(), 4);

-- 初級クイズの問題2: CSSの基本
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1), 
'CSSでテキストの色を赤色に設定するプロパティと値の正しい組み合わせはどれですか？', 
'multiple_choice', 
'色を指定するCSSプロパティを考えてみましょう', 
'color プロパティは要素のテキスト色を設定します。red は基本的な色名の一つで、#ff0000 や rgb(255,0,0) でも同じ赤色を表現できます。', 
1, 2, NOW());

-- 初級問題2の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 2),
'color: red;', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 2),
'text-color: red;', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 2),
'background: red;', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 2),
'font-color: red;', false, NOW(), 4);

-- 初級クイズの問題3: HTMLのリスト
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1), 
'HTMLで番号付きリスト（順序付きリスト）を作成するために使用するタグはどれですか？', 
'multiple_choice', 
'数字が自動的に付与されるリストのタグです', 
'<ol>（Ordered List）は番号付きリストを作成します。<ul>は番号なしリスト、<li>は各リスト項目を表します。', 
1, 3, NOW());

-- 初級問題3の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 3),
'<ol>', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 3),
'<ul>', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 3),
'<list>', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 3),
'<li>', false, NOW(), 4);

-- 初級クイズの問題4: CSSセレクタ
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1), 
'CSSでクラス名「menu」が付いた要素を選択するセレクタはどれですか？', 
'multiple_choice', 
'クラスセレクタは特定の記号から始まります', 
'クラスセレクタは「.」（ドット）で始まります。.menu は class="menu" が指定された全ての要素を選択します。', 
1, 4, NOW());

-- 初級問題4の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 4),
'.menu', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 4),
'#menu', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 4),
'menu', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 4),
'@menu', false, NOW(), 4);

-- 初級クイズの問題5: HTMLの画像タグ
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1), 
'HTMLで画像を表示するために使用するタグはどれですか？', 
'multiple_choice', 
'Image（画像）の略称がタグ名になっています', 
'<img>タグは画像を表示するために使用します。src属性で画像ファイルのパスを指定し、alt属性で代替テキストを設定します。', 
1, 5, NOW());

-- 初級問題5の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 5),
'<img>', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 5),
'<image>', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 5),
'<pic>', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 5),
'<photo>', false, NOW(), 4);

-- 3. 中級レベルの問題作成（レイアウト、Flexbox、レスポンシブデザイン）

-- 中級クイズの問題1: Flexbox
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2), 
'CSSのFlexboxで、アイテムを横方向（主軸）に中央揃えするプロパティと値はどれですか？', 
'multiple_choice', 
'justify-content プロパティの値を考えてみましょう', 
'justify-content: center; は Flexbox の主軸（通常は横方向）でアイテムを中央揃えします。align-items は交差軸の配置を制御します。', 
2, 1, NOW());

-- 中級問題1の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 1),
'justify-content: center;', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 1),
'align-items: center;', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 1),
'text-align: center;', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 1),
'flex-align: center;', false, NOW(), 4);

-- 中級クイズの問題2: CSS Grid
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2), 
'CSS Gridで3列のグリッドレイアウトを作成するプロパティと値はどれですか？', 
'multiple_choice', 
'グリッドのテンプレート列を定義するプロパティです', 
'grid-template-columns: 1fr 1fr 1fr; または repeat(3, 1fr) で3列の等幅グリッドを作成できます。1frは利用可能なスペースの1分割を表します。', 
2, 2, NOW());

-- 中級問題2の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 2),
'grid-template-columns: 1fr 1fr 1fr;', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 2),
'grid-columns: 3;', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 2),
'column-count: 3;', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 2),
'flex-columns: 3;', false, NOW(), 4);

-- 中級クイズの問題3: レスポンシブデザイン
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2), 
'CSSのメディアクエリで、画面幅が768px以下の場合にスタイルを適用するための正しい記述はどれですか？', 
'multiple_choice', 
'max-width を使って最大幅を指定します', 
'@media (max-width: 768px) はビューポートの幅が768px以下の場合にスタイルを適用します。レスポンシブデザインの基本的な記述方法です。', 
2, 3, NOW());

-- 中級問題3の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 3),
'@media (max-width: 768px)', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 3),
'@media (width <= 768px)', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 3),
'@responsive (max-width: 768px)', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 3),
'@screen (width: 768px)', false, NOW(), 4);

-- 中級クイズの問題4: CSS擬似クラス
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2), 
'リンクにマウスを乗せたときのスタイルを指定するCSS擬似クラスはどれですか？', 
'multiple_choice', 
'マウスを「乗せる」という動作に対応する擬似クラスです', 
':hover 擬似クラスはマウスカーソルが要素上にある間のスタイルを指定します。インタラクティブなUI作成に重要な要素です。', 
2, 4, NOW());

-- 中級問題4の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 4),
':hover', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 4),
':focus', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 4),
':active', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 4),
':visited', false, NOW(), 4);

-- 中級クイズの問題5: positionプロパティ  
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2), 
'CSSのpositionプロパティで、スクロールしても常に画面の同じ位置に固定表示するための値はどれですか？', 
'multiple_choice', 
'「固定」を意味する英単語がヒントです', 
'position: fixed; は要素をビューポートに対して固定位置に配置します。スクロールしても位置が変わらず、ヘッダーやフローティングボタンなどによく使用されます。', 
2, 5, NOW());

-- 中級問題5の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 5),
'fixed', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 5),
'absolute', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 5),
'relative', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 5),
'static', false, NOW(), 4);

COMMIT;

-- 結果確認用クエリ
SELECT q.title, d.name as difficulty, COUNT(qu.id) as question_count
FROM quiz_quiz q 
JOIN quiz_difficultylevel d ON q.difficulty_id = d.id
LEFT JOIN quiz_question qu ON q.id = qu.quiz_id
WHERE q.category_id = 1
GROUP BY q.id, q.title, d.name, d.level
ORDER BY d.level; -- HTML & CSSクイズ問題作成スクリプト（上級レベル）
-- 上級レベルの問題を追加

BEGIN;

-- 4. 上級レベルの問題作成（CSSアニメーション、詳細プロパティ、複雑なセレクタ）

-- 上級クイズの問題1: CSSアニメーション
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3), 
'CSSで2秒間かけて要素を回転させるアニメーションを作成する場合の正しい記述はどれですか？', 
'multiple_choice', 
'transform プロパティと transition を組み合わせます', 
'transition: transform 2s; と transform: rotate(360deg); を組み合わせることで、2秒間かけて要素を360度回転させるアニメーションを作成できます。', 
3, 1, NOW());

-- 上級問題1の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 1),
'transition: transform 2s; transform: rotate(360deg);', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 1),
'animation: rotate 2s; rotate: 360deg;', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 1),
'transform-duration: 2s; transform: rotate;', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 1),
'rotate-animation: 2s 360deg;', false, NOW(), 4);

-- 上級クイズの問題2: CSS変数（カスタムプロパティ）
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3), 
'CSS変数（カスタムプロパティ）を定義し、使用する正しい記述はどれですか？', 
'multiple_choice', 
'CSS変数は--で始まり、var()で使用します', 
'CSS変数は --変数名 で定義し、var(--変数名) で使用します。:root で定義すると全体で使用でき、保守性が向上します。', 
3, 2, NOW());

-- 上級問題2の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 2),
':root { --primary-color: blue; } .text { color: var(--primary-color); }', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 2),
'$primary-color: blue; .text { color: $primary-color; }', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 2),
'@define primary-color: blue; .text { color: @primary-color; }', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 2),
'#primary-color: blue; .text { color: #primary-color; }', false, NOW(), 4);

-- 上級クイズの問題3: CSS詳細セレクタ
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3), 
'ul要素の直接の子要素であるli要素のみを選択するCSSセレクタはどれですか？', 
'multiple_choice', 
'直接の子要素を表す記号は「>」です', 
'ul > li は ul の直接の子要素である li のみを選択します。ul li（スペース区切り）だと孫要素以下の li も選択してしまいます。', 
3, 3, NOW());

-- 上級問題3の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 3),
'ul > li', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 3),
'ul li', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 3),
'ul + li', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 3),
'ul ~ li', false, NOW(), 4);

-- 上級クイズの問題4: Flexboxの詳細プロパティ
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3), 
'Flexboxで特定のアイテムだけを残りスペースいっぱいに広げるプロパティはどれですか？', 
'multiple_choice', 
'アイテムの伸び縮みを制御するプロパティです', 
'flex-grow: 1; を特定のアイテムに適用すると、そのアイテムが残りのスペースを占有して広がります。他のアイテムは元のサイズを保持します。', 
3, 4, NOW());

-- 上級問題4の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 4),
'flex-grow: 1;', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 4),
'flex-expand: true;', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 4),
'width: auto;', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 4),
'stretch: 1;', false, NOW(), 4);

-- 上級クイズの問題5: CSS Gridの複雑なレイアウト
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3), 
'CSS Gridで要素を2行2列にまたがって配置するプロパティの組み合わせはどれですか？', 
'multiple_choice', 
'grid-column と grid-row を使ってスパンを指定します', 
'grid-column: span 2; と grid-row: span 2; で要素を2列2行にまたがって配置できます。span キーワードは指定した数のグリッドトラックにまたがることを意味します。', 
3, 5, NOW());

-- 上級問題5の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 5),
'grid-column: span 2; grid-row: span 2;', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 5),
'grid-area: 2x2;', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 5),
'grid-size: 2 2;', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 5),
'colspan: 2; rowspan: 2;', false, NOW(), 4);

COMMIT;

-- 結果確認用クエリ
SELECT 
    q.title, 
    d.name as difficulty, 
    COUNT(qu.id) as question_count,
    SUM(qu.points) as total_points
FROM quiz_quiz q 
JOIN quiz_difficultylevel d ON q.difficulty_id = d.id
LEFT JOIN quiz_question qu ON q.id = qu.quiz_id
WHERE q.category_id = 1
GROUP BY q.id, q.title, d.name, d.level
ORDER BY d.level; 

-- =========================================================
-- 統計情報・活動履歴を自動更新するトリガー
-- =========================================================

-- updated_at 更新用関数が既に存在する場合を考慮して CREATE OR REPLACE
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

    -- ヘルパー: 統計行を upsert
    PERFORM 1 FROM (
        SELECT NULL AS category_id, NULL AS difficulty_id UNION ALL
        SELECT category_id_val, NULL UNION ALL
        SELECT NULL, difficulty_id_val UNION ALL
        SELECT category_id_val, difficulty_id_val
    ) AS combos(cat_id, diff_id)
    WHERE TRUE;

    -- 全体／カテゴリ／難易度／カテゴリ×難易度それぞれを処理
    INSERT INTO quiz_userstatistics (
        user_id, category_id, difficulty_id,
        quizzes_completed, total_points, avg_score, highest_score, last_quiz_date
    ) VALUES
        (NEW.user_id, NULL, NULL, 1, NEW.score, NEW.percentage, NEW.score, NEW.completed_at),
        (NEW.user_id, category_id_val, NULL, 1, NEW.score, NEW.percentage, NEW.score, NEW.completed_at),
        (NEW.user_id, NULL, difficulty_id_val, 1, NEW.score, NEW.percentage, NEW.score, NEW.completed_at),
        (NEW.user_id, category_id_val, difficulty_id_val, 1, NEW.score, NEW.percentage, NEW.score, NEW.completed_at)
    ON CONFLICT (user_id, category_id, difficulty_id)
    DO UPDATE SET
        quizzes_completed = quiz_userstatistics.quizzes_completed + 1,
        total_points       = quiz_userstatistics.total_points + NEW.score,
        avg_score          = (quiz_userstatistics.avg_score * quiz_userstatistics.quizzes_completed + NEW.percentage) / (quiz_userstatistics.quizzes_completed + 1),
        highest_score      = GREATEST(quiz_userstatistics.highest_score, NEW.score),
        last_quiz_date     = NEW.completed_at,
        updated_at         = NOW();

    -- 活動履歴を追加
    INSERT INTO quiz_activityhistory (
        user_id, quiz_id, category_id, difficulty_id,
        score, percentage, activity_type, activity_date
    ) VALUES (
        NEW.user_id, NEW.quiz_id, category_id_val, difficulty_id_val,
        NEW.score, NEW.percentage, 'quiz_completed', NEW.completed_at
    );

    RETURN NEW;
END;
$$ language 'plpgsql';

-- トリガー本体（重複作成を避けるために存在確認）
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_trigger WHERE tgname = 'trigger_update_user_statistics'
    ) THEN
        CREATE TRIGGER trigger_update_user_statistics
            AFTER INSERT ON quiz_quizresult
            FOR EACH ROW
            EXECUTE FUNCTION update_user_statistics_on_quiz_result();
    END IF;
END;
$$; 