-- 本番データベースにクイズデータを追加するマイグレーション
-- 既存のファイルに統合されたデータを新しいバージョンで本番に反映

BEGIN;

-- HTML & CSS 初級問題の残り4問を追加 (2-5問目)
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 LIMIT 1), 
'CSSでテキストの色を赤色に設定するプロパティと値の正しい組み合わせはどれですか？', 
'multiple_choice', 
'色を指定するCSSプロパティを考えてみましょう', 
'color プロパティは要素のテキスト色を設定します。red は基本的な色名の一つで、#ff0000 や rgb(255,0,0) でも同じ赤色を表現できます。', 
1, 2, NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 LIMIT 1) AND display_order = 2 ORDER BY id LIMIT 1),
'color: red;', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 LIMIT 1) AND display_order = 2 ORDER BY id LIMIT 1),
'text-color: red;', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 LIMIT 1) AND display_order = 2 ORDER BY id LIMIT 1),
'background: red;', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 LIMIT 1) AND display_order = 2 ORDER BY id LIMIT 1),
'font-color: red;', false, NOW(), 4)
ON CONFLICT DO NOTHING;

-- 問題3: HTMLのリスト
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 LIMIT 1), 
'HTMLで番号付きリスト（順序付きリスト）を作成するために使用するタグはどれですか？', 
'multiple_choice', 
'数字が自動的に付与されるリストのタグです', 
'<ol>（Ordered List）は番号付きリストを作成します。<ul>は番号なしリスト、<li>は各リスト項目を表します。', 
1, 3, NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 LIMIT 1) AND display_order = 3 ORDER BY id LIMIT 1),
'<ol>', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 LIMIT 1) AND display_order = 3 ORDER BY id LIMIT 1),
'<ul>', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 LIMIT 1) AND display_order = 3 ORDER BY id LIMIT 1),
'<list>', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 LIMIT 1) AND display_order = 3 ORDER BY id LIMIT 1),
'<li>', false, NOW(), 4)
ON CONFLICT DO NOTHING;

-- 問題4: CSSセレクタ
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 LIMIT 1), 
'CSSでクラス名「menu」が付いた要素を選択するセレクタはどれですか？', 
'multiple_choice', 
'クラスセレクタは特定の記号から始まります', 
'クラスセレクタは「.」（ドット）で始まります。.menu は class="menu" が指定された全ての要素を選択します。', 
1, 4, NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 LIMIT 1) AND display_order = 4 ORDER BY id LIMIT 1),
'.menu', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 LIMIT 1) AND display_order = 4 ORDER BY id LIMIT 1),
'#menu', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 LIMIT 1) AND display_order = 4 ORDER BY id LIMIT 1),
'menu', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 LIMIT 1) AND display_order = 4 ORDER BY id LIMIT 1),
'@menu', false, NOW(), 4)
ON CONFLICT DO NOTHING;

-- 問題5: HTMLの画像タグ
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 LIMIT 1), 
'HTMLで画像を表示するために使用するタグはどれですか？', 
'multiple_choice', 
'Image（画像）の略称がタグ名になっています', 
'<img>タグは画像を表示するために使用します。src属性で画像ファイルのパスを指定し、alt属性で代替テキストを設定します。', 
1, 5, NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 LIMIT 1) AND display_order = 5 ORDER BY id LIMIT 1),
'<img>', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 LIMIT 1) AND display_order = 5 ORDER BY id LIMIT 1),
'<image>', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 LIMIT 1) AND display_order = 5 ORDER BY id LIMIT 1),
'<pic>', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1 LIMIT 1) AND display_order = 5 ORDER BY id LIMIT 1),
'<photo>', false, NOW(), 4)
ON CONFLICT DO NOTHING;

-- HTML & CSS 中級問題（全5問）
-- 問題1: Flexbox
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1), 
'CSSのFlexboxで、アイテムを横方向（主軸）に中央揃えするプロパティと値はどれですか？', 
'multiple_choice', 
'justify-content プロパティの値を考えてみましょう', 
'justify-content: center; は Flexbox の主軸（通常は横方向）でアイテムを中央揃えします。align-items は交差軸の配置を制御します。', 
2, 1, NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1) AND display_order = 1 ORDER BY id LIMIT 1),
'justify-content: center;', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1) AND display_order = 1 ORDER BY id LIMIT 1),
'align-items: center;', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1) AND display_order = 1 ORDER BY id LIMIT 1),
'text-align: center;', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1) AND display_order = 1 ORDER BY id LIMIT 1),
'flex-align: center;', false, NOW(), 4)
ON CONFLICT DO NOTHING;

-- 問題2: CSS Grid
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1), 
'CSS Gridで3列のグリッドレイアウトを作成するプロパティと値はどれですか？', 
'multiple_choice', 
'グリッドのテンプレート列を定義するプロパティです', 
'grid-template-columns: 1fr 1fr 1fr; または repeat(3, 1fr) で3列の等幅グリッドを作成できます。1frは利用可能なスペースの1分割を表します。', 
2, 2, NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1) AND display_order = 2 ORDER BY id LIMIT 1),
'grid-template-columns: 1fr 1fr 1fr;', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1) AND display_order = 2 ORDER BY id LIMIT 1),
'grid-columns: 3;', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1) AND display_order = 2 ORDER BY id LIMIT 1),
'column-count: 3;', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1) AND display_order = 2 ORDER BY id LIMIT 1),
'flex-columns: 3;', false, NOW(), 4)
ON CONFLICT DO NOTHING;

-- 問題3: レスポンシブデザイン
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1), 
'CSSのメディアクエリで、画面幅が768px以下の場合にスタイルを適用するための正しい記述はどれですか？', 
'multiple_choice', 
'max-width を使って最大幅を指定します', 
'@media (max-width: 768px) はビューポートの幅が768px以下の場合にスタイルを適用します。レスポンシブデザインの基本的な記述方法です。', 
2, 3, NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1) AND display_order = 3 ORDER BY id LIMIT 1),
'@media (max-width: 768px)', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1) AND display_order = 3 ORDER BY id LIMIT 1),
'@media (width <= 768px)', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1) AND display_order = 3 ORDER BY id LIMIT 1),
'@responsive (max-width: 768px)', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1) AND display_order = 3 ORDER BY id LIMIT 1),
'@screen (width: 768px)', false, NOW(), 4)
ON CONFLICT DO NOTHING;

-- 問題4: CSS擬似クラス
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1), 
'リンクにマウスを乗せたときのスタイルを指定するCSS擬似クラスはどれですか？', 
'multiple_choice', 
'マウスを「乗せる」という動作に対応する擬似クラスです', 
':hover 擬似クラスはマウスカーソルが要素上にある間のスタイルを指定します。インタラクティブなUI作成に重要な要素です。', 
2, 4, NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1) AND display_order = 4 ORDER BY id LIMIT 1),
':hover', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1) AND display_order = 4 ORDER BY id LIMIT 1),
':focus', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1) AND display_order = 4 ORDER BY id LIMIT 1),
':active', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1) AND display_order = 4 ORDER BY id LIMIT 1),
':visited', false, NOW(), 4)
ON CONFLICT DO NOTHING;

-- 問題5: positionプロパティ  
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1), 
'CSSのpositionプロパティで、スクロールしても常に画面の同じ位置に固定表示するための値はどれですか？', 
'multiple_choice', 
'「固定」を意味する英単語がヒントです', 
'position: fixed; は要素をビューポートに対して固定位置に配置します。スクロールしても位置が変わらず、ヘッダーやフローティングボタンなどによく使用されます。', 
2, 5, NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1) AND display_order = 5 ORDER BY id LIMIT 1),
'fixed', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1) AND display_order = 5 ORDER BY id LIMIT 1),
'absolute', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1) AND display_order = 5 ORDER BY id LIMIT 1),
'relative', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2 LIMIT 1) AND display_order = 5 ORDER BY id LIMIT 1),
'static', false, NOW(), 4)
ON CONFLICT DO NOTHING;

-- Ruby 初級問題（全5問）
-- 問題1: puts
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1 LIMIT 1),
'Rubyでコンソールに文字列を改行付きで出力するメソッドはどれですか？','multiple_choice','標準出力に文字列を書き込み、末尾に改行を追加します','puts メソッドは与えられた文字列を改行付きで出力します。',1,1,NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1 LIMIT 1) AND display_order=1 ORDER BY id LIMIT 1),'puts',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1 LIMIT 1) AND display_order=1 ORDER BY id LIMIT 1),'print',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1 LIMIT 1) AND display_order=1 ORDER BY id LIMIT 1),'echo',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1 LIMIT 1) AND display_order=1 ORDER BY id LIMIT 1),'console.log',false,NOW(),4)
ON CONFLICT DO NOTHING;

-- 問題2: nil
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1 LIMIT 1),
'Rubyで「値が存在しない」ことを表すオブジェクトはどれですか？','multiple_choice','他言語の null に相当します','nil は Ruby で「何もない」ことを示す唯一のオブジェクトです。',1,2,NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1 LIMIT 1) AND display_order=2 ORDER BY id LIMIT 1),'nil',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1 LIMIT 1) AND display_order=2 ORDER BY id LIMIT 1),'null',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1 LIMIT 1) AND display_order=2 ORDER BY id LIMIT 1),'None',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1 LIMIT 1) AND display_order=2 ORDER BY id LIMIT 1),'undefined',false,NOW(),4)
ON CONFLICT DO NOTHING;

-- 問題3: push
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1 LIMIT 1),
'Rubyで配列の末尾に要素を追加するメソッドはどれですか？','multiple_choice','<< 演算子のエイリアスです','push メソッド（または << 演算子）を使って配列末尾に要素を追加します。',1,3,NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1 LIMIT 1) AND display_order=3 ORDER BY id LIMIT 1),'push',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1 LIMIT 1) AND display_order=3 ORDER BY id LIMIT 1),'add',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1 LIMIT 1) AND display_order=3 ORDER BY id LIMIT 1),'append',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1 LIMIT 1) AND display_order=3 ORDER BY id LIMIT 1),'insert',false,NOW(),4)
ON CONFLICT DO NOTHING;

-- 問題4: 文字列連結
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1 LIMIT 1),
'Rubyで文字列を連結する演算子はどれですか？','multiple_choice','足し算と同じ記号です','Ruby では + 演算子で文字列連結ができます。',1,4,NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1 LIMIT 1) AND display_order=4 ORDER BY id LIMIT 1),'+',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1 LIMIT 1) AND display_order=4 ORDER BY id LIMIT 1),'&',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1 LIMIT 1) AND display_order=4 ORDER BY id LIMIT 1),'.',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1 LIMIT 1) AND display_order=4 ORDER BY id LIMIT 1),'=>',false,NOW(),4)
ON CONFLICT DO NOTHING;

-- 問題5: pop
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1 LIMIT 1),
'Rubyで配列の最後の要素を取り出して削除するメソッドはどれですか？','multiple_choice','shift は先頭要素を返します','pop メソッドで末尾要素を返して削除できます。',1,5,NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1 LIMIT 1) AND display_order=5 ORDER BY id LIMIT 1),'pop',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1 LIMIT 1) AND display_order=5 ORDER BY id LIMIT 1),'delete',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1 LIMIT 1) AND display_order=5 ORDER BY id LIMIT 1),'remove_last',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=1 LIMIT 1) AND display_order=5 ORDER BY id LIMIT 1),'slice!',false,NOW(),4)
ON CONFLICT DO NOTHING;

-- Ruby 中級問題（全5問）
-- 問題1: map メソッドの戻り値
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2 LIMIT 1),
'Enumerable#map メソッドを呼び出したときの戻り値として正しいものはどれですか？',
'multiple_choice',
'変換結果を保持します',
'map はブロックの戻り値を要素として持つ「新しい配列」を返します。元の配列は変化しません。',
2,1,NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2 LIMIT 1) AND display_order=1 ORDER BY id LIMIT 1),'ブロック結果を要素とする新しい配列',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2 LIMIT 1) AND display_order=1 ORDER BY id LIMIT 1),'nil',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2 LIMIT 1) AND display_order=1 ORDER BY id LIMIT 1),'self と同じ配列',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2 LIMIT 1) AND display_order=1 ORDER BY id LIMIT 1),'Enumerator オブジェクト',false,NOW(),4)
ON CONFLICT DO NOTHING;

-- 問題2: &: 記法
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2 LIMIT 1),
'Array#map(&:to_s) の &: 記法が内部で実行している処理はどれですか？',
'multiple_choice',
'Proc オブジェクトに変換します',
'&:symbol は Symbol#to_proc を呼び出してブロックに変換し、要素に対してメソッド呼び出しを行います。',
2,2,NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2 LIMIT 1) AND display_order=2 ORDER BY id LIMIT 1),'Symbol#to_proc でブロックを生成して呼び出す',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2 LIMIT 1) AND display_order=2 ORDER BY id LIMIT 1),'each に書き換えて実行',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2 LIMIT 1) AND display_order=2 ORDER BY id LIMIT 1),'メタプログラミングでメソッドを定義',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2 LIMIT 1) AND display_order=2 ORDER BY id LIMIT 1),'特別な構文糖で RubyVM が最適化',false,NOW(),4)
ON CONFLICT DO NOTHING;

-- 問題3: 例外処理の継承順
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2 LIMIT 1),
'rescue 節で複数の例外クラスを書く場合、評価順として正しいのはどれですか？',
'multiple_choice',
'より具体的な例外から書きます',
'上位クラスを先に書くと下位クラスに到達せず捕捉されないため、具体的（サブクラス）→一般的（スーパークラス）の順に記述します。',
2,3,NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2 LIMIT 1) AND display_order=3 ORDER BY id LIMIT 1),'サブクラスを先、スーパークラスを後',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2 LIMIT 1) AND display_order=3 ORDER BY id LIMIT 1),'スーパークラスを先、サブクラスを後',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2 LIMIT 1) AND display_order=3 ORDER BY id LIMIT 1),'アルファベット順',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2 LIMIT 1) AND display_order=3 ORDER BY id LIMIT 1),'記述順は影響しない',false,NOW(),4)
ON CONFLICT DO NOTHING;

-- 問題4: attr_accessor
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2 LIMIT 1),
'`attr_accessor :name` をクラスに定義すると生成されるメソッドの組み合わせはどれですか？',
'multiple_choice',
'読み取りと書き込み',
'attr_accessor は同名のゲッターとセッターを定義します。インスタンス変数 @name に対するアクセスを簡略化します。',
2,4,NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2 LIMIT 1) AND display_order=4 ORDER BY id LIMIT 1),'name と name=',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2 LIMIT 1) AND display_order=4 ORDER BY id LIMIT 1),'get_name と set_name',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2 LIMIT 1) AND display_order=4 ORDER BY id LIMIT 1),'initialize と to_s',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2 LIMIT 1) AND display_order=4 ORDER BY id LIMIT 1),'name? と name!',false,NOW(),4)
ON CONFLICT DO NOTHING;

-- 問題5: include と extend
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2 LIMIT 1),
'Module を mixin する際、インスタンスメソッドとして追加するキーワードはどれですか？',
'multiple_choice',
'クラスに「混ぜる」イメージ',
'include はモジュールのメソッドをインスタンスメソッドとして、extend はクラスメソッドとして追加します。',
2,5,NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2 LIMIT 1) AND display_order=5 ORDER BY id LIMIT 1),'include',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2 LIMIT 1) AND display_order=5 ORDER BY id LIMIT 1),'extend',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2 LIMIT 1) AND display_order=5 ORDER BY id LIMIT 1),'prepend',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=2 LIMIT 1) AND display_order=5 ORDER BY id LIMIT 1),'require',false,NOW(),4)
ON CONFLICT DO NOTHING;

-- Ruby 上級問題（全5問）
-- 問題1: method_missing
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3 LIMIT 1),
'クラスで `def method_missing(name, *args); end` をオーバーライドしたとき、暗黙で **呼び出されなくなる** メソッドフックはどれですか？',
'multiple_choice',
'無限再帰を避けるために分かれています',
'respond_to_missing? は method_missing と対になるフックで、メソッド応答判定に使われます。method_missing を定義しても respond_to_missing? が自動定義されることはありません。',
3,1,NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3 LIMIT 1) AND display_order=1 ORDER BY id LIMIT 1),'respond_to_missing?',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3 LIMIT 1) AND display_order=1 ORDER BY id LIMIT 1),'initialize_copy',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3 LIMIT 1) AND display_order=1 ORDER BY id LIMIT 1),'method_added',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3 LIMIT 1) AND display_order=1 ORDER BY id LIMIT 1),'included',false,NOW(),4)
ON CONFLICT DO NOTHING;

-- 問題2: eigenclass
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3 LIMIT 1),
'次のコードで `self` が指すオブジェクトは何ですか？\n```ruby\nobj = "hello"\nclass << obj\n  self\nend\n```',
'multiple_choice',
'単独の特異クラス',
'`class << obj` は obj の特異クラス（eigenclass）をオープンします。よって self はその特異クラスを指します。',
3,2,NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3 LIMIT 1) AND display_order=2 ORDER BY id LIMIT 1),'obj の特異クラス',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3 LIMIT 1) AND display_order=2 ORDER BY id LIMIT 1),'String クラス',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3 LIMIT 1) AND display_order=2 ORDER BY id LIMIT 1),'obj 自身 ("hello")',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3 LIMIT 1) AND display_order=2 ORDER BY id LIMIT 1),'main オブジェクト',false,NOW(),4)
ON CONFLICT DO NOTHING;

-- 問題3: refine
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3 LIMIT 1),
'Ruby の Refinements 機能を有効化するキーワードはどれですか？',
'multiple_choice',
'using 〇〇',
'Refinements を有効にするには `using モジュール名` をソースのトップレベルかクラス/モジュール定義内で呼び出します。',
3,3,NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3 LIMIT 1) AND display_order=3 ORDER BY id LIMIT 1),'using',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3 LIMIT 1) AND display_order=3 ORDER BY id LIMIT 1),'import',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3 LIMIT 1) AND display_order=3 ORDER BY id LIMIT 1),'include',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3 LIMIT 1) AND display_order=3 ORDER BY id LIMIT 1),'extend',false,NOW(),4)
ON CONFLICT DO NOTHING;

-- 問題4: Fiber#resume の戻り値
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3 LIMIT 1),
'Fiber#resume を呼び出したとき、呼び出し側に返る値として正しいものはどれですか？',
'multiple_choice',
'yield と同様のイメージ',
'Fiber#resume は Fiber 内で `yield`（または最終値）によって外に渡されたオブジェクトを返します。',
3,4,NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3 LIMIT 1) AND display_order=4 ORDER BY id LIMIT 1),'Fiber 内から yield された値',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3 LIMIT 1) AND display_order=4 ORDER BY id LIMIT 1),'nil 固定',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3 LIMIT 1) AND display_order=4 ORDER BY id LIMIT 1),'Fiber オブジェクト自身',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3 LIMIT 1) AND display_order=4 ORDER BY id LIMIT 1),'次に resume で渡す引数',false,NOW(),4)
ON CONFLICT DO NOTHING;

-- 問題5: prepend
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3 LIMIT 1),
'Module#prepend を使ってモジュールをミックスインした場合のメソッド探索順として正しいものはどれですか？',
'multiple_choice',
'prepend は「先頭に挿入」',
'prepend はモジュールをクラスの祖先チェーンの先頭に挿入するため、そのモジュールのメソッドがクラスの同名メソッドより優先します。',
3,5,NOW())
ON CONFLICT DO NOTHING;

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3 LIMIT 1) AND display_order=5 ORDER BY id LIMIT 1),'モジュール → クラス → 既存の祖先',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3 LIMIT 1) AND display_order=5 ORDER BY id LIMIT 1),'クラス → モジュール → 既存の祖先',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3 LIMIT 1) AND display_order=5 ORDER BY id LIMIT 1),'既存の祖先 → クラス → モジュール',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=2 AND difficulty_id=3 LIMIT 1) AND display_order=5 ORDER BY id LIMIT 1),'モジュールは探索に含まれない',false,NOW(),4)
ON CONFLICT DO NOTHING;

COMMIT;

-- 結果確認用クエリ
SELECT '✅ 本番データベースにクイズデータ追加完了' as status;
SELECT 'HTML&CSS初級問題数: ' || COUNT(*) as html_css_beginner FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 1);
SELECT 'HTML&CSS中級問題数: ' || COUNT(*) as html_css_intermediate FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 1 AND difficulty_id = 2);
SELECT 'Ruby初級問題数: ' || COUNT(*) as ruby_beginner FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1);
SELECT 'Ruby中級問題数: ' || COUNT(*) as ruby_intermediate FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2);
SELECT 'Ruby上級問題数: ' || COUNT(*) as ruby_advanced FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3); 