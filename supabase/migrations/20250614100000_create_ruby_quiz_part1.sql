-- Ruby クイズ問題作成スクリプト
-- カテゴリID: 2 (Ruby)
-- 3つの難易度レベルそれぞれにクイズを作成

BEGIN;

-- 1. クイズの作成
INSERT INTO quiz_quiz (category_id, difficulty_id, title, description, time_limit, pass_score, is_active, created_at, updated_at) VALUES
-- 初級クイズ
(2, 1, 'Ruby 基礎', 'Rubyの基本的な構文とデータ型について学びましょう', 300, 70, true, NOW(), NOW()),
-- 中級クイズ
(2, 2, 'Ruby 中級', 'Enumerableや例外処理、シンボルなど中級レベルの機能を学びましょう', 600, 70, true, NOW(), NOW()),
-- 上級クイズ
(2, 3, 'Ruby 応用', 'メタプログラミングや高度な言語機能に挑戦しましょう', 900, 70, true, NOW(), NOW());

-- 2. 初級レベルの問題作成（基本構文・データ型）

-- 問題1: puts
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1),
'Rubyでコンソールに文字列を改行付きで出力するメソッドはどれですか？',
'multiple_choice',
'標準出力に文字列を書き込み、末尾に改行を追加します',
'puts メソッドは与えられた文字列を出力し、末尾に自動的に\n（改行）を付加します。',
1, 1, NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 1), 'puts', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 1), 'print', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 1), 'echo', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 1), 'console.log', false, NOW(), 4);

-- 問題2: nil キーワード
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1),
'Rubyで「値が存在しない」ことを表すオブジェクトはどれですか？',
'multiple_choice',
'他の言語でいう null に相当します',
'nil は Ruby で「何もない」ことを示す唯一のオブジェクトです。nil は FalseClass にも属し、条件分岐で false 扱いになります。',
1, 2, NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 2), 'nil', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 2), 'null', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 2), 'None', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 2), 'undefined', false, NOW(), 4);

-- 問題3: 配列 push
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1),
'Rubyで配列の末尾に要素を追加する最も一般的なメソッドはどれですか？',
'multiple_choice',
'<< 演算子のエイリアスでもあります',
'push メソッド（または << 演算子）を使うと、配列の末尾に要素を追加できます。',
1, 3, NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 3), 'push', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 3), 'add', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 3), 'append', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 3), 'insert', false, NOW(), 4);

-- 問題4: 文字列連結
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1),
'Rubyで文字列を連結する演算子はどれですか？',
'multiple_choice',
'足し算と同じ記号です',
'Ruby では + 演算子を使って文字列を連結できます。また、<< や concat メソッドも使用できますが、最も基本的なのは + です。',
1, 4, NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 4), '+', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 4), '&', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 4), '.', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 4), '=>', false, NOW(), 4);

-- 問題5: pop
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1),
'Rubyで配列の最後の要素を取り出して削除するメソッドはどれですか？',
'multiple_choice',
'対になるメソッド shift は先頭要素を取り出します',
'pop メソッドを呼び出すと、配列の末尾要素を返して同時に削除します。',
1, 5, NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 5), 'pop', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 5), 'delete', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 5), 'remove_last', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 1) AND display_order = 5), 'slice!', false, NOW(), 4);

-- 3. 中級レベルの問題作成（Enumerable・例外処理・シンボル 等）

-- 中級 問題1: map
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2),
'Rubyで各要素を変換して新しい配列を返すメソッドはどれですか？',
'multiple_choice',
'ブロックで変換を定義します',
'map は各要素をブロックの戻り値で置き換え、新しい配列を返します。同義の collect メソッドもあります。',
2, 1, NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 1), 'map', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 1), 'each', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 1), 'inject', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 1), 'filter', false, NOW(), 4);

-- 中級 問題2: all?
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2),
'RubyのEnumerableモジュールで、全ての要素が条件を満たすか調べるメソッドはどれですか？',
'multiple_choice',
'条件が一つでも偽だと false を返します',
'all? はブロック内の条件を全要素が満たす場合に true を返します。',
2, 2, NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 2), 'all?', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 2), 'any?', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 2), 'none?', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 2), 'find', false, NOW(), 4);

-- 中級 問題3: rescue
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2),
'Rubyで例外を捕捉する際に使用するキーワードはどれですか？',
'multiple_choice',
'begin ... ? ... end の形で使います',
'rescue は例外処理構文の一部で、発生した例外を捕捉して適切に処理します。',
2, 3, NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 3), 'rescue', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 3), 'catch', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 3), 'except', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 3), 'handle', false, NOW(), 4);

-- 中級 問題4: シンボル表記
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2),
'Rubyでシンボルを定義する際の正しいリテラル表記はどれですか？',
'multiple_choice',
'シンボルはコロンから始まります',
':symbol_name の形式で表され、イミュータブルで軽量な識別子として使われます。',
2, 4, NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 4), ':user', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 4), 'user:', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 4), '"user"', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 4), ':user()', false, NOW(), 4);

-- 中級 問題5: attr_accessor
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2),
'Rubyでインスタンス変数の読み書きを簡単に定義できるメソッドはどれですか？',
'multiple_choice',
'getter と setter を同時に生成します',
'attr_accessor は attr_reader と attr_writer を組み合わせたメソッドで、読み書き可能なアクセサを生成します。',
2, 5, NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 5), 'attr_accessor', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 5), 'attr_reader', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 5), 'attr_writer', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 2) AND display_order = 5), 'accessor', false, NOW(), 4);

-- 4. 上級レベルの問題作成（メタプログラミング・モジュール 等）

-- 上級 問題1: include
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3),
'Rubyでモジュールのインスタンスメソッドをクラスに取り込むためのキーワードはどれですか？',
'multiple_choice',
'クラスにメソッドを「混ぜ込む」操作です',
'include を使うとモジュールのインスタンスメソッドがクラスのインスタンスメソッドとして利用できるようになります。',
3, 1, NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 1), 'include', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 1), 'extend', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 1), 'prepend', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 1), 'require', false, NOW(), 4);

-- 上級 問題2: extend
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3),
'Rubyでモジュールのメソッドをクラスのクラスメソッドとして取り込むキーワードはどれですか？',
'multiple_choice',
'クラス自身にメソッドを追加します',
'extend を使うとモジュールのメソッドがクラスメソッドとして追加されます。',
3, 2, NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 2), 'extend', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 2), 'include', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 2), 'mixin', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 2), 'prepend', false, NOW(), 4);

-- 上級 問題3: prepend
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3),
'Rubyでモジュールのインスタンスメソッドをクラスに「先頭に」取り込むキーワードはどれですか？',
'multiple_choice',
'include との違いに注目しましょう',
'prepend を使うと、モジュールのメソッドがクラスのメソッドよりも優先されて呼び出されます。メソッドのフックや装飾に利用されます。',
3, 3, NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 3), 'prepend', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 3), 'include', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 3), 'extend', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 3), 'alias', false, NOW(), 4);

-- 上級 問題4: method_missing
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3),
'Rubyで未定義メソッド呼び出しを動的に処理するためにオーバーライドするメソッドはどれですか？',
'multiple_choice',
'動的ディスパッチに利用されます',
'method_missing をオーバーライドすると、存在しないメソッド呼び出しを補足して動的に処理できます。メタプログラミングの代表的なテクニックです。',
3, 4, NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 4), 'method_missing', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 4), 'respond_to?', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 4), 'define_method', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 4), 'send', false, NOW(), 4);

-- 上級 問題5: alias_method
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3),
'Rubyで既存メソッドの別名を作成し、元のメソッドを上書きせずにラップする際によく使われるメソッドはどれですか？',
'multiple_choice',
'メソッド名のエイリアスを作ります',
'alias_method を使うと、元のメソッド名を保持したまま新しい名前で呼び出せるようになります。メソッドチェーンの前後で処理を追加する際などに利用されます。',
3, 5, NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 5), 'alias_method', true, NOW(), 1),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 5), 'define_method', false, NOW(), 2),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 5), 'prepend', false, NOW(), 3),
((SELECT id FROM quiz_question WHERE quiz_id = (SELECT id FROM quiz_quiz WHERE category_id = 2 AND difficulty_id = 3) AND display_order = 5), 'override', false, NOW(), 4);

COMMIT;