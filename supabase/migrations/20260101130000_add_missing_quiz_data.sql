-- 本番データベースに不足している全てのクイズデータを追加
-- seed.sqlの完全なデータセットに基づく修正版

BEGIN;

-- HTML & CSS 初級問題の残り4問を追加 (2-5問目)
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

-- HTML & CSS 中級問題を全て追加 (1-5問目)
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

-- Rubyクイズ用テーブルを追加
INSERT INTO quiz_quiz (category_id, difficulty_id, title, description, time_limit, pass_score, is_active, thumbnail_url, banner_image_url, media_type, created_at, updated_at) VALUES
(2, 1, 'Ruby 基礎', 'Rubyの基本的な構文とデータ型について学びましょう', 300, 70, true, 'https://placehold.co/300x200?text=Ruby+Beginner', 'https://placehold.co/600x200?text=Ruby+Banner', 'image', NOW(), NOW()),
(2, 2, 'Ruby 中級', 'Enumerableや例外処理、シンボルなど中級レベルの機能を学びましょう', 600, 70, true, 'https://placehold.co/300x200?text=Ruby+Intermediate', 'https://placehold.co/600x200?text=Ruby+Banner', 'image', NOW(), NOW()),
(2, 3, 'Ruby 応用', 'メタプログラミングや高度な言語機能に挑戦しましょう', 900, 70, true, 'https://placehold.co/300x200?text=Ruby+Advanced', 'https://placehold.co/600x200?text=Ruby+Banner', 'image', NOW(), NOW());

-- Ruby初級問題を追加
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1),
'Rubyでコンソールに文字列を改行付きで出力するメソッドはどれですか？','multiple_choice','標準出力に文字列を書き込み、末尾に改行を追加します','puts メソッドは与えられた文字列を改行付きで出力します。',1,1,NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=1),'puts',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=1),'print',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=1),'echo',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1) AND display_order=1),'console.log',false,NOW(),4);

COMMIT; 