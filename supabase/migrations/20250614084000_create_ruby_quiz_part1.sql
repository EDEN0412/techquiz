-- Ruby クイズ問題作成スクリプト
-- カテゴリID: 2 (Ruby)
-- 難易度: 初級(1), 中級(2), 上級(3)

BEGIN;

-- 1. クイズの作成
INSERT INTO quiz_quiz (category_id, difficulty_id, title, description, time_limit, pass_score, is_active, created_at, updated_at) VALUES
-- 初級クイズ
(2, 1, 'Ruby 基礎', 'Rubyの基本的な構文とデータ型について学びましょう', 300, 70, true, NOW(), NOW()),
-- 中級クイズ
(2, 2, 'Ruby 中級', 'Enumerableや例外処理、シンボルなど中級レベルの機能を学びましょう', 600, 70, true, NOW(), NOW()),
-- 上級クイズ
(2, 3, 'Ruby 応用', 'メタプログラミングやパフォーマンス最適化など上級トピックに挑戦しましょう', 900, 70, true, NOW(), NOW());

-- =========================================
-- 初級レベル (難易度ID:1) 各5問
-- =========================================

-- 問題1: puts
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1),
'Rubyでコンソールに文字列を改行付きで出力するメソッドはどれですか？',
'multiple_choice',
'標準出力に文字列を書き込み、末尾に改行を追加します',
'puts メソッドは与えられた文字列を出力し、末尾に自動的に\n（改行）を付加します。',
1, 1, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 1), 'puts', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 1), 'print', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 1), 'echo', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 1), 'console.log', false, NOW());

-- 問題2: length
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1),
'Rubyで配列の要素数を取得するメソッドはどれですか？',
'multiple_choice',
'配列サイズを取得する標準メソッドです',
'length メソッドは配列や文字列の要素数（長さ）を返します。',
1, 2, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 2), 'length', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 2), 'size', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 2), 'count', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 2), 'elements', false, NOW());

-- 問題3: if
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1),
'Rubyで条件分岐を行うための基本的なキーワードはどれですか？',
'multiple_choice',
'他の言語でもよく使われるキーワードです',
'if は条件が真の場合に処理を実行する基本的な制御構造です。',
1, 3, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 3), 'if', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 3), 'when', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 3), 'switch', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 3), 'choose', false, NOW());

-- 問題4: {}
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1),
'Rubyでハッシュリテラルを作成するときに使用する囲い記号はどれですか？',
'multiple_choice',
'キーと値のペアを囲む記号です',
'ハッシュリテラルは { key: value } のように "{ }" で囲んで表現します。',
1, 4, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 4), '{ }', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 4), '[ ]', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 4), '( )', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 4), '< >', false, NOW());

-- 問題5: each
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1),
'Rubyで配列の各要素に対して順番に処理を行うメソッドはどれですか？',
'multiple_choice',
'ブロックを受け取り、要素を順に渡します',
'each メソッドは配列やハッシュなどの各要素に対してブロックを実行します。',
1, 5, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 5), 'each', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 5), 'loop', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 5), 'for', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 5), 'iterate', false, NOW());

-- =========================================
-- 中級レベル (難易度ID:2) 各5問
-- =========================================

-- 問題1: all?
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2),
'RubyのEnumerableモジュールで、全ての要素が条件を満たすか調べるメソッドはどれですか？',
'multiple_choice',
'条件が一つでも偽だとfalseを返します',
'all? はブロック内の条件を全要素が満たす場合にtrueを返します。',
2, 1, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 1), 'all?', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 1), 'any?', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 1), 'select', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 1), 'map', false, NOW());

-- 問題2: rescue
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2),
'Rubyで例外を捕捉する際に使用するキーワードはどれですか？',
'multiple_choice',
'begin ... ? ... end の形で使います',
'rescue は例外処理構文の一部で、発生した例外を捕捉して適切に処理します。',
2, 2, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 2), 'rescue', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 2), 'catch', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 2), 'handle', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 2), 'except', false, NOW());

-- 問題3: :symbol
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2),
'Rubyでシンボルを定義する際の正しいリテラル表記はどれですか？',
'multiple_choice',
'シンボルはコロンから始まります',
':symbol_name の形式で表され、イミュータブルで軽量な識別子として使われます。',
2, 3, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 3), ':user', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 3), '"user"', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 3), 'user:', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 3), ':user()', false, NOW());

-- 問題4: map
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2),
'Rubyで各要素を変換して新しい配列を返すメソッドはどれですか？',
'multiple_choice',
'ブロックで変換を定義します',
'map は各要素をブロックの戻り値で置き換え、新しい配列を返します。',
2, 4, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 4), 'map', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 4), 'each', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 4), 'collect!', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 4), 'inject', false, NOW());

-- 問題5: nil?
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2),
'オブジェクトがnilかどうかを判定するRubyのメソッドはどれですか？',
'multiple_choice',
'nilチェック専用メソッドです',
'nil? メソッドはレシーバが nil の場合に true を返します。',
2, 5, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 5), 'nil?', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 5), 'empty?', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 5), 'blank?', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 5), 'zero?', false, NOW());

-- =========================================
-- 上級レベル (難易度ID:3) 各5問
-- =========================================

-- 問題1: include
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3),
'Rubyでモジュールのインスタンスメソッドをクラスに取り込むためのキーワードはどれですか？',
'multiple_choice',
'クラスにメソッドを「混ぜ込む」操作です',
'include を使うとモジュールのインスタンスメソッドがクラスのインスタンスメソッドとして利用できるようになります。',
3, 1, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 1), 'include', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 1), 'extend', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 1), 'prepend', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 1), 'require', false, NOW());

-- 問題2: extend
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3),
'Rubyでモジュールのメソッドをクラスのクラスメソッドとして取り込むキーワードはどれですか？',
'multiple_choice',
'クラス自身にメソッドを追加します',
'extend を使うとモジュールのメソッドがクラスメソッドとして追加されます。',
3, 2, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 2), 'extend', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 2), 'include', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 2), 'inherit', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 2), 'mix', false, NOW());

-- 問題3: define_method
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3),
'Rubyのメタプログラミングで、ランタイムにインスタンスメソッドを生成するメソッドはどれですか？',
'multiple_choice',
'"define_〇〇_method" の形です',
'define_method はブロックを受け取り、実行時にメソッドを定義できます。',
3, 3, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 3), 'define_method', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 3), 'method_missing', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 3), 'alias_method', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 3), 'define_singleton_method', false, NOW());

-- 問題4: Mark and Sweep
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3),
'Rubyで主に採用されているガベージコレクション方式はどれですか？',
'multiple_choice',
'不要オブジェクトを「印付け」して回収します',
'Ruby MRI は基本的にマーク＆スイープ方式を採用しており、不要になったオブジェクトを検出してメモリを解放します。',
3, 4, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 4), 'マーク＆スイープ', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 4), '参照カウント', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 4), 'コピーオンライト', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 4), '世代別GC', false, NOW());

-- 問題5: Enumerator::Lazy
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3),
'Rubyで遅延評価により大規模データを効率的に処理するために使用されるクラスはどれですか？',
'multiple_choice',
'Enumerator クラスのサブクラスです',
'Enumerator::Lazy はチェーンメソッドを遅延評価し、必要になるまで要素を計算しません。',
3, 5, NOW());

INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 5), 'Enumerator::Lazy', true, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 5), 'Fiber', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 5), 'Thread', false, NOW()),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 5), 'Enumerator', false, NOW());

COMMIT;