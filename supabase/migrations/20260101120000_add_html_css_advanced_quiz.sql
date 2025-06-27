-- HTML & CSS 上級レベルの問題を追加するマイグレーション
-- 本番環境で不足している上級問題（5問）を追加します

BEGIN;

-- 上級クイズの問題1: CSS Transform
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3), 
'CSSのtransformプロパティで要素を水平方向に100px、垂直方向に50px移動させる記述はどれですか？', 
'multiple_choice', 
'translate関数を使用します', 
'transform: translate(100px, 50px); で要素を指定した距離だけ移動できます。第1引数がX軸（水平）、第2引数がY軸（垂直）方向の移動量です。', 
3, 1, NOW());

-- 上級問題1の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 1),
'transform: translate(100px, 50px);', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 1),
'transform: move(100px, 50px);', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 1),
'position: translate(100px, 50px);', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 1),
'transform: position(100px, 50px);', false, NOW(), 4);

-- 上級クイズの問題2: CSS変数（カスタムプロパティ）
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3), 
'CSS変数（カスタムプロパティ）を定義し、使用する正しい記述はどれですか？', 
'multiple_choice', 
'-- で始まり、var()で使用します', 
'CSS変数は --variable-name で定義し、var(--variable-name) で使用します。再利用可能で動的な値の管理に便利です。', 
3, 2, NOW());

-- 上級問題2の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 2),
':root { --main-color: blue; } .element { color: var(--main-color); }', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 2),
':root { $main-color: blue; } .element { color: $(main-color); }', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 2),
':root { main-color: blue; } .element { color: var(main-color); }', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 2),
':root { --main-color: blue; } .element { color: main-color; }', false, NOW(), 4);

-- 上級クイズの問題3: CSS nth-child擬似クラス
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3), 
'CSS疑似クラスで「3番目以降の偶数番目の要素」を選択するセレクタはどれですか？', 
'multiple_choice', 
'nth-child()で計算式を使用します', 
':nth-child(2n+2) または :nth-child(even):nth-child(n+3) で3番目以降の偶数番目要素を選択できます。nは0から始まる自然数です。', 
3, 3, NOW());

-- 上級問題3の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 3),
':nth-child(2n+2)', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 3),
':nth-child(3n+2)', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 3),
':nth-child(even+3)', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 3),
':nth-child(2n-1)', false, NOW(), 4);

-- 上級クイズの問題4: CSS calc()関数
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3), 
'CSS calc()関数で「ビューポート幅から40pxを引いた値」を設定する正しい記述はどれですか？', 
'multiple_choice', 
'異なる単位間で計算ができます', 
'calc(100vw - 40px) でビューポート幅から40pxを引いた値を計算できます。演算子の前後にはスペースが必要です。', 
3, 4, NOW());

-- 上級問題4の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 4),
'calc(100vw - 40px)', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 4),
'calc(100vw-40px)', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 4),
'calc(100% - 40px)', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 4),
'calculate(100vw - 40px)', false, NOW(), 4);

-- 上級クイズの問題5: CSS Grid Template Areas
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3), 
'CSS Gridで名前付きエリアを定義するプロパティはどれですか？', 
'multiple_choice', 
'テンプレートとエリアがキーワードです', 
'grid-template-areas プロパティで名前付きグリッドエリアを定義し、grid-area プロパティで要素を配置します。', 
3, 5, NOW());

-- 上級問題5の回答選択肢
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 5),
'grid-template-areas', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 5),
'grid-area-template', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 5),
'grid-areas', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 3) AND display_order = 5),
'grid-template-names', false, NOW(), 4);

COMMIT; 