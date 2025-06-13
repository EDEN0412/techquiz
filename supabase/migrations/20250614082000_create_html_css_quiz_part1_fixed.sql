-- HTML & CSSクイズ問題作成スクリプト
-- カテゴリID: 1 (HTML & CSS)
-- 3つの難易度レベルそれぞれにクイズを作成

BEGIN;

-- 1. クイズの作成
INSERT INTO quiz_quiz (category_id, difficulty_id, title, description, time_limit, pass_score, is_active, created_at, updated_at) VALUES
-- 初級クイズ
(1, 1, 'HTML & CSS 基礎', 'HTMLとCSSの基本的なタグとプロパティについて学びましょう', 300, 70, true, NOW(), NOW()),
-- 中級クイズ  
(1, 2, 'HTML & CSS レイアウト', 'FlexboxやGridを使ったレイアウト技法とレスポンシブデザインについて学びましょう', 600, 70, true, NOW(), NOW()),
-- 上級クイズ
(1, 3, 'HTML & CSS 応用', 'CSS詳細プロパティとアニメーション、複雑なレイアウト技法について学びましょう', 900, 70, true, NOW(), NOW());

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
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 1),
'<title>', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 1),
'<header>', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 1),
'<h1>', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 1),
'<meta>', false, NOW());

-- 初級クイズの問題2: CSSの基本
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1), 
'CSSでテキストの色を赤色に設定するプロパティと値の正しい組み合わせはどれですか？', 
'multiple_choice', 
'色を指定するCSSプロパティを考えてみましょう', 
'color プロパティは要素のテキスト色を設定します。red は基本的な色名の一つで、#ff0000 や rgb(255,0,0) でも同じ赤色を表現できます。', 
1, 2, NOW());

-- 初級問題2の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 2),
'color: red;', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 2),
'text-color: red;', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 2),
'background: red;', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 2),
'font-color: red;', false, NOW());

-- 初級クイズの問題3: HTMLのリスト
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1), 
'HTMLで番号付きリスト（順序付きリスト）を作成するために使用するタグはどれですか？', 
'multiple_choice', 
'数字が自動的に付与されるリストのタグです', 
'<ol>（Ordered List）は番号付きリストを作成します。<ul>は番号なしリスト、<li>は各リスト項目を表します。', 
1, 3, NOW());

-- 初級問題3の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 3),
'<ol>', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 3),
'<ul>', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 3),
'<list>', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 3),
'<li>', false, NOW());

-- 初級クイズの問題4: CSSセレクタ
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1), 
'CSSでクラス名「menu」が付いた要素を選択するセレクタはどれですか？', 
'multiple_choice', 
'クラスセレクタは特定の記号から始まります', 
'クラスセレクタは「.」（ドット）で始まります。.menu は class="menu" が指定された全ての要素を選択します。', 
1, 4, NOW());

-- 初級問題4の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 4),
'.menu', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 4),
'#menu', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 4),
'menu', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 4),
'@menu', false, NOW());

-- 初級クイズの問題5: HTMLの画像タグ
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1), 
'HTMLで画像を表示するために使用するタグはどれですか？', 
'multiple_choice', 
'Image（画像）の略称がタグ名になっています', 
'<img>タグは画像を表示するために使用します。src属性で画像ファイルのパスを指定し、alt属性で代替テキストを設定します。', 
1, 5, NOW());

-- 初級問題5の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 5),
'<img>', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 5),
'<image>', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 5),
'<pic>', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1) AND display_order = 5),
'<photo>', false, NOW());

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
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 1),
'justify-content: center;', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 1),
'align-items: center;', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 1),
'text-align: center;', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 1),
'flex-align: center;', false, NOW());

-- 中級クイズの問題2: CSS Grid
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2), 
'CSS Gridで3列のグリッドレイアウトを作成するプロパティと値はどれですか？', 
'multiple_choice', 
'グリッドのテンプレート列を定義するプロパティです', 
'grid-template-columns: 1fr 1fr 1fr; または repeat(3, 1fr) で3列の等幅グリッドを作成できます。1frは利用可能なスペースの1分割を表します。', 
2, 2, NOW());

-- 中級問題2の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 2),
'grid-template-columns: 1fr 1fr 1fr;', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 2),
'grid-columns: 3;', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 2),
'column-count: 3;', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 2),
'flex-columns: 3;', false, NOW());

-- 中級クイズの問題3: レスポンシブデザイン
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2), 
'CSSのメディアクエリで、画面幅が768px以下の場合にスタイルを適用するための正しい記述はどれですか？', 
'multiple_choice', 
'max-width を使って最大幅を指定します', 
'@media (max-width: 768px) はビューポートの幅が768px以下の場合にスタイルを適用します。レスポンシブデザインの基本的な記述方法です。', 
2, 3, NOW());

-- 中級問題3の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 3),
'@media (max-width: 768px)', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 3),
'@media (width <= 768px)', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 3),
'@responsive (max-width: 768px)', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 3),
'@screen (width: 768px)', false, NOW());

-- 中級クイズの問題4: CSS擬似クラス
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2), 
'リンクにマウスを乗せたときのスタイルを指定するCSS擬似クラスはどれですか？', 
'multiple_choice', 
'マウスを「乗せる」という動作に対応する擬似クラスです', 
':hover 擬似クラスはマウスカーソルが要素上にある間のスタイルを指定します。インタラクティブなUI作成に重要な要素です。', 
2, 4, NOW());

-- 中級問題4の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 4),
':hover', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 4),
':focus', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 4),
':active', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 4),
':visited', false, NOW());

-- 中級クイズの問題5: positionプロパティ  
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2), 
'CSSのpositionプロパティで、スクロールしても常に画面の同じ位置に固定表示するための値はどれですか？', 
'multiple_choice', 
'「固定」を意味する英単語がヒントです', 
'position: fixed; は要素をビューポートに対して固定位置に配置します。スクロールしても位置が変わらず、ヘッダーやフローティングボタンなどによく使用されます。', 
2, 5, NOW());

-- 中級問題5の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 5),
'fixed', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 5),
'absolute', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 5),
'relative', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2) AND display_order = 5),
'static', false, NOW());

COMMIT;

-- 結果確認用クエリ
SELECT q.title, d.name as difficulty, COUNT(qu.id) as question_count
FROM quiz_quiz q 
JOIN quiz_difficultylevel d ON q.difficulty_id = d.id
LEFT JOIN quiz_question qu ON q.id = qu.quiz_id
WHERE q.category_id = 1
GROUP BY q.id, q.title, d.name, d.level
ORDER BY d.level; 