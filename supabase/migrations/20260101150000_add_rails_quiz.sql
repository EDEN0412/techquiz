-- Railsクイズ（カテゴリID:3）追加マイグレーション
-- 2026-01-01 15:00:00

BEGIN;

-- 1. クイズの作成
INSERT INTO quiz_quiz (category_id, difficulty_id, title, description, time_limit, pass_score, is_active, thumbnail_url, banner_image_url, media_type, created_at, updated_at) VALUES
-- 初級クイズ
(3, 1, 'Rails on rails 初級', 'Railsの基本構造やコマンドについて学びましょう', 300, 70, true, 'https://placehold.co/300x200?text=Rails+Beginner', 'https://placehold.co/600x200?text=Rails+Banner', 'image', NOW(), NOW()),
-- 中級クイズ
(3, 2, 'Rails on rails 中級', 'ActiveRecordやバリデーション、関連付けなど中級レベルの機能を学びましょう', 600, 70, true, 'https://placehold.co/300x200?text=Rails+Intermediate', 'https://placehold.co/600x200?text=Rails+Banner', 'image', NOW(), NOW()),
-- 上級クイズ
(3, 3, 'Rails on rails 上級', 'コールバックやStrong Parameters、N+1問題など応用的な内容に挑戦しましょう', 900, 70, true, 'https://placehold.co/300x200?text=Rails+Advanced', 'https://placehold.co/600x200?text=Rails+Banner', 'image', NOW(), NOW());

-- 2. 初級レベルの問題作成
-- 問題1
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 3 AND difficulty_id = 1),
'RailsのMVCで「C」は何を指しますか？','multiple_choice','MVCのCは何の略か考えましょう','MVCはModel-View-Controllerの略で、CはController（コントローラー）を指します。',1,1,NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=1) AND display_order=1),'Controller',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=1) AND display_order=1),'Command',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=1) AND display_order=1),'Component',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=1) AND display_order=1),'Configuration',false,NOW(),4);
-- 問題2
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 3 AND difficulty_id = 1),
'Railsで新しいプロジェクトを作成するコマンドは？','multiple_choice','rails new コマンドを思い出しましょう','rails new プロジェクト名 で新しいRailsアプリを作成します。',1,2,NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=1) AND display_order=2),'rails new',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=1) AND display_order=2),'rails start',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=1) AND display_order=2),'rails create',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=1) AND display_order=2),'rails init',false,NOW(),4);
-- 問題3
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 3 AND difficulty_id = 1),
'Railsでデータベースのマイグレーションを実行するコマンドは？','multiple_choice','db:migrate コマンドを思い出しましょう','rails db:migrate でマイグレーションを実行します。',1,3,NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=1) AND display_order=3),'rails db:migrate',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=1) AND display_order=3),'rails migrate',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=1) AND display_order=3),'rails db:update',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=1) AND display_order=3),'rails db:run',false,NOW(),4);
-- 問題4
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 3 AND difficulty_id = 1),
'Railsでモデルを作成するコマンドは？','multiple_choice','generate model コマンドを思い出しましょう','rails generate model モデル名 でモデルを作成します。',1,4,NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=1) AND display_order=4),'rails generate model',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=1) AND display_order=4),'rails make model',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=1) AND display_order=4),'rails create model',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=1) AND display_order=4),'rails new model',false,NOW(),4);
-- 問題5
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 3 AND difficulty_id = 1),
'Railsでルーティングを設定するファイルは？','multiple_choice','routes.rb ファイルを思い出しましょう','ルーティングはconfig/routes.rbで設定します。',1,5,NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=1) AND display_order=5),'config/routes.rb',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=1) AND display_order=5),'app/routes.rb',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=1) AND display_order=5),'routes/config.rb',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=1) AND display_order=5),'app/config/routes.rb',false,NOW(),4);

-- 3. 中級レベルの問題作成
-- 問題1
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 3 AND difficulty_id = 2),
'RailsのActiveRecordで、全てのレコードを取得するメソッドは？','multiple_choice','all メソッドを思い出しましょう','Model.all で全レコードを取得します。',2,1,NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=2) AND display_order=1),'all',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=2) AND display_order=1),'find',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=2) AND display_order=1),'get',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=2) AND display_order=1),'fetch',false,NOW(),4);
-- 問題2
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 3 AND difficulty_id = 2),
'Railsでバリデーションを追加する場所は？','multiple_choice','バリデーションはどこに書くか思い出しましょう','バリデーションはモデルに記述します。',2,2,NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=2) AND display_order=2),'モデル',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=2) AND display_order=2),'コントローラー',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=2) AND display_order=2),'ビュー',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=2) AND display_order=2),'ルーティング',false,NOW(),4);
-- 問題3
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 3 AND difficulty_id = 2),
'Railsで「1対多」の関連を表すメソッドは？','multiple_choice','has_many メソッドを思い出しましょう','has_manyで1対多の関係を表します。',2,3,NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=2) AND display_order=3),'has_many',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=2) AND display_order=3),'belongs_to',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=2) AND display_order=3),'has_one',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=2) AND display_order=3),'has_and_belongs_to_many',false,NOW(),4);
-- 問題4
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 3 AND difficulty_id = 2),
'Railsでマイグレーションファイルを取り消すコマンドは？','multiple_choice','db:rollback コマンドを思い出しましょう','rails db:rollback で直前のマイグレーションを取り消します。',2,4,NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=2) AND display_order=4),'rails db:rollback',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=2) AND display_order=4),'rails db:reset',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=2) AND display_order=4),'rails db:undo',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=2) AND display_order=4),'rails db:remove',false,NOW(),4);
-- 問題5
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 3 AND difficulty_id = 2),
'Railsで部分テンプレートを呼び出すメソッドは？','multiple_choice','render メソッドを思い出しましょう','render partial: \'ファイル名\' で部分テンプレートを呼び出します。',2,5,NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=2) AND display_order=5),'render',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=2) AND display_order=5),'partial',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=2) AND display_order=5),'include',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=2) AND display_order=5),'require',false,NOW(),4);

-- 4. 上級レベルの問題作成
-- 問題1
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 3 AND difficulty_id = 3),
'Railsのコールバックで、レコード保存前に実行されるものは？','multiple_choice','before_save コールバックを思い出しましょう','before_saveは保存前に実行されるコールバックです。',3,1,NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=3) AND display_order=1),'before_save',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=3) AND display_order=1),'after_save',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=3) AND display_order=1),'before_destroy',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=3) AND display_order=1),'after_create',false,NOW(),4);
-- 問題2
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 3 AND difficulty_id = 3),
'RailsのStrong Parametersは何のために使いますか？','multiple_choice','パラメータのホワイトリスト化を思い出しましょう','Strong Parametersは許可したパラメータのみを受け取るための仕組みです。',3,2,NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=3) AND display_order=2),'パラメータのホワイトリスト化',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=3) AND display_order=2),'ルーティングの設定',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=3) AND display_order=2),'モデルの関連付け',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=3) AND display_order=2),'ビューのレンダリング',false,NOW(),4);
-- 問題3
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 3 AND difficulty_id = 3),
'RailsでN+1問題を解決するためのメソッドは？','multiple_choice','includes メソッドを思い出しましょう','includesを使うことで関連テーブルをまとめて取得し、N+1問題を防ぎます。',3,3,NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=3) AND display_order=3),'includes',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=3) AND display_order=3),'joins',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=3) AND display_order=3),'select',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=3) AND display_order=3),'group',false,NOW(),4);
-- 問題4
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 3 AND difficulty_id = 3),
'Railsのconcernは何のために使いますか？','multiple_choice','共通処理の再利用を思い出しましょう','concernは共通処理をまとめて再利用するための仕組みです。',3,4,NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=3) AND display_order=4),'複数のモデルやコントローラーで共通の機能をまとめる',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=3) AND display_order=4),'データベースの接続設定',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=3) AND display_order=4),'ルーティングのグループ化',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=3) AND display_order=4),'ビューのキャッシュ',false,NOW(),4);
-- 問題5
INSERT INTO quiz_question (quiz_id, question_text, question_type, hint, explanation, points, display_order, created_at) VALUES
((SELECT id FROM quiz_quiz WHERE category_id = 3 AND difficulty_id = 3),
'RailsでAPI専用アプリを作成するコマンドは？','multiple_choice','--api オプションを思い出しましょう','rails new アプリ名 --api でAPI専用のRailsアプリを作成します。',3,5,NOW());
INSERT INTO quiz_answer (question_id, answer_text, is_correct, created_at, display_order) VALUES
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=3) AND display_order=5),'rails new アプリ名 --api',true,NOW(),1),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=3) AND display_order=5),'rails new アプリ名 --only-api',false,NOW(),2),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=3) AND display_order=5),'rails generate api',false,NOW(),3),
((SELECT id FROM quiz_question WHERE quiz_id=(SELECT id FROM quiz_quiz WHERE category_id=3 AND difficulty_id=3) AND display_order=5),'rails api new',false,NOW(),4);

COMMIT; 