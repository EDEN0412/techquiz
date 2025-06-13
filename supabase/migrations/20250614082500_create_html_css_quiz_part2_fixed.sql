-- HTML & CSSクイズ問題作成スクリプト（上級レベル）
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
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 1),
'transition: transform 2s; transform: rotate(360deg);', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 1),
'animation: rotate 2s; rotate: 360deg;', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 1),
'transform-duration: 2s; transform: rotate;', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 1),
'rotate-animation: 2s 360deg;', false, NOW());

-- 上級クイズの問題2: CSS変数（カスタムプロパティ）
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3), 
'CSS変数（カスタムプロパティ）を定義し、使用する正しい記述はどれですか？', 
'multiple_choice', 
'CSS変数は--で始まり、var()で使用します', 
'CSS変数は --変数名 で定義し、var(--変数名) で使用します。:root で定義すると全体で使用でき、保守性が向上します。', 
3, 2, NOW());

-- 上級問題2の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 2),
':root { --primary-color: blue; } .text { color: var(--primary-color); }', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 2),
'$primary-color: blue; .text { color: $primary-color; }', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 2),
'@define primary-color: blue; .text { color: @primary-color; }', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 2),
'#primary-color: blue; .text { color: #primary-color; }', false, NOW());

-- 上級クイズの問題3: CSS詳細セレクタ
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3), 
'ul要素の直接の子要素であるli要素のみを選択するCSSセレクタはどれですか？', 
'multiple_choice', 
'直接の子要素を表す記号は「>」です', 
'ul > li は ul の直接の子要素である li のみを選択します。ul li（スペース区切り）だと孫要素以下の li も選択してしまいます。', 
3, 3, NOW());

-- 上級問題3の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 3),
'ul > li', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 3),
'ul li', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 3),
'ul + li', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 3),
'ul ~ li', false, NOW());

-- 上級クイズの問題4: Flexboxの詳細プロパティ
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3), 
'Flexboxで特定のアイテムだけを残りスペースいっぱいに広げるプロパティはどれですか？', 
'multiple_choice', 
'アイテムの伸び縮みを制御するプロパティです', 
'flex-grow: 1; を特定のアイテムに適用すると、そのアイテムが残りのスペースを占有して広がります。他のアイテムは元のサイズを保持します。', 
3, 4, NOW());

-- 上級問題4の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 4),
'flex-grow: 1;', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 4),
'flex-expand: true;', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 4),
'width: auto;', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 4),
'stretch: 1;', false, NOW());

-- 上級クイズの問題5: CSS Gridの複雑なレイアウト
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3), 
'CSS Gridで要素を2行2列にまたがって配置するプロパティの組み合わせはどれですか？', 
'multiple_choice', 
'grid-column と grid-row を使ってスパンを指定します', 
'grid-column: span 2; と grid-row: span 2; で要素を2列2行にまたがって配置できます。span キーワードは指定した数のグリッドトラックにまたがることを意味します。', 
3, 5, NOW());

-- 上級問題5の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 5),
'grid-column: span 2; grid-row: span 2;', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 5),
'grid-area: 2x2;', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 5),
'grid-size: 2 2;', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 5),
'colspan: 2; rowspan: 2;', false, NOW());

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