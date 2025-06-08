"""
シリアライザーのテスト
"""

import unittest
from datetime import datetime
from django.test import TestCase
from django.contrib.auth import get_user_model
from quiz.models import (
    Category, DifficultyLevel, Quiz, Question, Answer, 
    QuizResult, UserStatistics, ActivityHistory
)
from quiz.serializers import (
    CategorySerializer, DifficultyLevelSerializer, 
    QuizSerializer, QuizDetailSerializer, QuestionSerializer, 
    AnswerSerializer, QuizResultSerializer, 
    UserStatisticsSerializer, ActivityHistorySerializer
)


class CategorySerializerTest(TestCase):
    """
    CategorySerializerのテスト
    """
    
    def setUp(self):
        """
        テスト前の準備
        """
        # テスト用のカテゴリデータを作成
        self.category_attributes = {
            'name': 'Pythonプログラミング',
            'slug': 'python-programming',
            'description': 'Pythonに関するクイズカテゴリです。',
            'icon': 'fab fa-python',
            'display_order': 1,
            'is_active': True
        }
        self.category = Category.objects.create(**self.category_attributes)
        self.serializer = CategorySerializer(instance=self.category)

    def test_contains_expected_fields(self):
        """
        シリアライザーが期待されるフィールドを含んでいるかテスト
        """
        data = self.serializer.data
        # データに含まれるキーのセットと、期待されるキーのセットが一致するか確認
        self.assertEqual(set(data.keys()), set([
            'id', 'name', 'slug', 'description', 'icon',
            'display_order', 'is_active', 'created_at', 'updated_at'
        ]))

    def test_field_content(self):
        """
        各フィールドの内容が正しいかテスト
        """
        data = self.serializer.data
        # 各フィールドの値を検証
        self.assertEqual(data['name'], self.category_attributes['name'])
        self.assertEqual(data['slug'], self.category_attributes['slug'])
        self.assertEqual(data['description'], self.category_attributes['description'])
        self.assertEqual(data['icon'], self.category_attributes['icon'])
        self.assertEqual(data['display_order'], self.category_attributes['display_order'])
        self.assertEqual(data['is_active'], self.category_attributes['is_active'])
        # created_atとupdated_atは自動生成されるので、存在するかのみ確認
        self.assertIsNotNone(data['created_at'])
        self.assertIsNotNone(data['updated_at'])

    def test_serialization_of_collection(self):
        """
        複数のカテゴリをシリアライズできるかテスト
        """
        category2_attributes = {
            'name': 'JavaScript基礎',
            'slug': 'javascript-basics',
            'description': 'JavaScriptの基本的な概念を学びます。',
            'icon': 'fab fa-js',
            'display_order': 2,
            'is_active': True
        }
        Category.objects.create(**category2_attributes)
        
        categories = Category.objects.all().order_by('display_order')
        serializer = CategorySerializer(categories, many=True)
        
        # 2つのカテゴリがシリアライズされることを確認
        self.assertEqual(len(serializer.data), 2)
        # 1つ目のカテゴリの内容を確認
        self.assertEqual(serializer.data[0]['name'], self.category_attributes['name'])
        # 2つ目のカテゴリの内容を確認
        self.assertEqual(serializer.data[1]['name'], category2_attributes['name'])

    def test_deserialization_valid_data(self):
        """
        有効なデータでデシリアライズできるかテスト
        """
        valid_serializer_data = {
            'name': '新しいカテゴリ',
            'slug': 'new-category',
            'description': 'テスト用の新しいカテゴリです。',
            'display_order': 3,
            'is_active': True
        }
        serializer = CategorySerializer(data=valid_serializer_data)
        # バリデーションが通ることを確認
        self.assertTrue(serializer.is_valid())
        # 保存して新しいカテゴリが作成されることを確認
        new_category = serializer.save()
        self.assertEqual(new_category.name, valid_serializer_data['name'])
        self.assertEqual(new_category.slug, valid_serializer_data['slug'])
        self.assertEqual(new_category.description, valid_serializer_data['description'])

    def test_read_only_fields(self):
        """
        read_only_fieldsが正しく機能するかテスト
        """
        # 既存オブジェクトを更新する場合
        update_data = {
            'name': '更新されたPython',
            'id': 999,  # これは無視されるべき
            'created_at': '2000-01-01T00:00:00Z',  # これも無視されるべき
            'updated_at': '2000-01-01T00:00:00Z'   # これも無視されるべき
        }
        serializer = CategorySerializer(instance=self.category, data=update_data, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_category = serializer.save()
        # nameは更新されるが、read_onlyフィールドは元の値のままであることを確認
        self.assertEqual(updated_category.name, update_data['name'])
        self.assertNotEqual(updated_category.id, 999)
        # created_atがupdated_atより前の時刻であることを確認（更新されていない）
        self.assertLess(
            datetime.fromisoformat(updated_category.created_at.isoformat()), 
            datetime.fromisoformat(updated_category.updated_at.isoformat())
        )

    def test_invalid_data_handling(self):
        """
        無効なデータの処理をテスト
        """
        # nameが空の場合（必須フィールドのバリデーション）
        invalid_data_empty_name = {
            'name': '',
            'slug': 'empty-name'
        }
        serializer = CategorySerializer(data=invalid_data_empty_name)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
        
        # slugが重複している場合（一意制約のバリデーション）
        invalid_data_duplicate_slug = {
            'name': '別のカテゴリ',
            'slug': self.category.slug  # 既存のslugを使用
        }
        serializer = CategorySerializer(data=invalid_data_duplicate_slug)
        self.assertFalse(serializer.is_valid())
        self.assertIn('slug', serializer.errors)


class DifficultyLevelSerializerTest(TestCase):
    """
    DifficultyLevelSerializerのテスト
    """
    
    def setUp(self):
        """
        テスト前の準備
        """
        # テスト用の難易度データを作成
        self.difficulty_attributes = {
            'name': '初級',
            'slug': 'beginner',
            'level': 1,
            'description': '初心者向けの難易度です。',
            'point_multiplier': 1,
            'time_limit': 300  # 5分
        }
        self.difficulty = DifficultyLevel.objects.create(**self.difficulty_attributes)
        self.serializer = DifficultyLevelSerializer(instance=self.difficulty)

    def test_contains_expected_fields(self):
        """
        シリアライザーが期待されるフィールドを含んでいるかテスト
        """
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set([
            'id', 'name', 'slug', 'level', 'description', 
            'point_multiplier', 'time_limit', 'created_at', 'updated_at'
        ]))

    def test_field_content(self):
        """
        各フィールドの内容が正しいかテスト
        """
        data = self.serializer.data
        self.assertEqual(data['name'], self.difficulty_attributes['name'])
        self.assertEqual(data['slug'], self.difficulty_attributes['slug'])
        self.assertEqual(data['level'], self.difficulty_attributes['level'])
        self.assertEqual(data['description'], self.difficulty_attributes['description'])
        self.assertEqual(data['point_multiplier'], self.difficulty_attributes['point_multiplier'])
        self.assertEqual(data['time_limit'], self.difficulty_attributes['time_limit'])
        self.assertIsNotNone(data['created_at'])
        self.assertIsNotNone(data['updated_at'])

    def test_deserialization_valid_data(self):
        """
        有効なデータでデシリアライズできるかテスト
        """
        valid_serializer_data = {
            'name': '中級',
            'slug': 'intermediate',
            'level': 2,
            'description': '中級者向けの難易度です。',
            'point_multiplier': 2,
            'time_limit': 600  # 10分
        }
        serializer = DifficultyLevelSerializer(data=valid_serializer_data)
        self.assertTrue(serializer.is_valid())
        new_difficulty = serializer.save()
        self.assertEqual(new_difficulty.name, valid_serializer_data['name'])
        self.assertEqual(new_difficulty.level, valid_serializer_data['level'])

    def test_invalid_data_handling(self):
        """
        無効なデータの処理をテスト
        """
        # levelが重複している場合（一意制約のバリデーション）
        invalid_data_duplicate_level = {
            'name': '別の初級',
            'slug': 'another-beginner',
            'level': self.difficulty.level  # 既存のlevelを使用
        }
        serializer = DifficultyLevelSerializer(data=invalid_data_duplicate_level)
        self.assertFalse(serializer.is_valid())
        self.assertIn('level', serializer.errors)


class QuizSerializerTest(TestCase):
    """
    QuizSerializerのテスト
    """
    
    def setUp(self):
        """
        テスト前の準備
        """
        # カテゴリーと難易度を作成
        self.category = Category.objects.create(
            name='Python基礎',
            slug='python-basics',
            description='Python言語の基本的な概念を学ぶ'
        )
        self.difficulty = DifficultyLevel.objects.create(
            name='初級',
            slug='beginner',
            level=1,
            point_multiplier=1
        )
        
        # テスト用のクイズデータを作成
        self.quiz_attributes = {
            'category': self.category,
            'difficulty': self.difficulty,
            'title': 'Python変数と型',
            'description': 'Pythonの変数と基本的なデータ型に関するクイズ',
            'time_limit': 600,
            'pass_score': 70,
            'is_active': True
        }
        self.quiz = Quiz.objects.create(**self.quiz_attributes)
        self.serializer = QuizSerializer(instance=self.quiz)

    def test_contains_expected_fields(self):
        """
        シリアライザーが期待されるフィールドを含んでいるかテスト
        """
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set([
            'id', 'category', 'category_name', 'difficulty', 'difficulty_name',
            'title', 'description', 'time_limit', 'pass_score', 'is_active',
            'thumbnail_url', 'banner_image_url', 'media_type', 
            'created_at', 'updated_at'
        ]))

    def test_serialized_data(self):
        """
        シリアライズされたデータの内容をテスト
        """
        data = self.serializer.data
        # 基本的なフィールドの検証
        self.assertEqual(data['title'], self.quiz_attributes['title'])
        self.assertEqual(data['description'], self.quiz_attributes['description'])
        self.assertEqual(data['time_limit'], self.quiz_attributes['time_limit'])
        self.assertEqual(data['pass_score'], self.quiz_attributes['pass_score'])
        self.assertEqual(data['is_active'], self.quiz_attributes['is_active'])
        
        # 関連オブジェクトのIDと名前の検証
        self.assertEqual(data['category'], self.category.id)
        self.assertEqual(data['category_name'], self.category.name)
        self.assertEqual(data['difficulty'], self.difficulty.id)
        self.assertEqual(data['difficulty_name'], self.difficulty.name)

    def test_deserialization_valid_data(self):
        """
        有効なデータでデシリアライズできるかテスト
        """
        # 新しいカテゴリーと難易度を作成
        new_category = Category.objects.create(
            name='Django Web開発',
            slug='django-web-dev',
            description='Django Webフレームワークについて学ぶ'
        )
        new_difficulty = DifficultyLevel.objects.create(
            name='中級',
            slug='intermediate',
            level=2,
            point_multiplier=2
        )
        
        valid_serializer_data = {
            'category': new_category.id,
            'difficulty': new_difficulty.id,
            'title': 'Django MVTパターン',
            'description': 'Django Model-View-Templateアーキテクチャについてのクイズ',
            'time_limit': 900,
            'pass_score': 75,
            'is_active': True
        }
        serializer = QuizSerializer(data=valid_serializer_data)
        self.assertTrue(serializer.is_valid())
        new_quiz = serializer.save()
        self.assertEqual(new_quiz.title, valid_serializer_data['title'])
        self.assertEqual(new_quiz.category.id, valid_serializer_data['category'])
        self.assertEqual(new_quiz.difficulty.id, valid_serializer_data['difficulty'])


class QuizDetailSerializerTest(TestCase):
    """
    QuizDetailSerializerのテスト（問題を含む）
    """
    
    def setUp(self):
        """
        テスト前の準備
        """
        # カテゴリーと難易度を作成
        self.category = Category.objects.create(
            name='Python基礎',
            slug='python-basics'
        )
        self.difficulty = DifficultyLevel.objects.create(
            name='初級',
            slug='beginner',
            level=1
        )
        
        # クイズを作成
        self.quiz = Quiz.objects.create(
            category=self.category,
            difficulty=self.difficulty,
            title='Python変数と型',
            description='Pythonの変数と基本的なデータ型に関するクイズ'
        )
        
        # 問題を作成
        self.question1 = Question.objects.create(
            quiz=self.quiz,
            question_text='Pythonで文字列を定義するには？',
            question_type='single_choice',
            points=10,
            display_order=1
        )
        
        self.question2 = Question.objects.create(
            quiz=self.quiz,
            question_text='Pythonの整数型は？',
            question_type='single_choice',
            points=10,
            display_order=2
        )
        
        # 回答を作成
        Answer.objects.create(
            question=self.question1,
            answer_text="'hello'",
            is_correct=True,
            display_order=1
        )
        Answer.objects.create(
            question=self.question1,
            answer_text="hello",
            is_correct=False,
            display_order=2
        )
        
        Answer.objects.create(
            question=self.question2,
            answer_text="int",
            is_correct=True,
            display_order=1
        )
        Answer.objects.create(
            question=self.question2,
            answer_text="float",
            is_correct=False,
            display_order=2
        )
        
        self.serializer = QuizDetailSerializer(instance=self.quiz)

    def test_contains_expected_fields(self):
        """
        シリアライザーが期待されるフィールドを含んでいるかテスト
        """
        data = self.serializer.data
        # QuizSerializerのフィールド + questionsフィールド
        expected_fields = set([
            'id', 'category', 'category_name', 'difficulty', 'difficulty_name',
            'title', 'description', 'time_limit', 'pass_score', 'is_active',
            'thumbnail_url', 'banner_image_url', 'media_type', 
            'created_at', 'updated_at', 'questions'
        ])
        self.assertEqual(set(data.keys()), expected_fields)

    def test_questions_are_included(self):
        """
        問題が正しく含まれているかテスト
        """
        data = self.serializer.data
        # 問題の数が正しいか確認
        self.assertEqual(len(data['questions']), 2)
        
        # 各問題のフィールドをチェック
        question1_data = data['questions'][0]
        self.assertEqual(question1_data['question_text'], self.question1.question_text)
        self.assertEqual(question1_data['question_type'], self.question1.question_type)
        
        # 回答が含まれているか確認
        self.assertEqual(len(question1_data['answers']), 2)
        
        # 回答の内容をチェック
        answer1 = question1_data['answers'][0]
        self.assertTrue(answer1['is_correct'])  # 最初の回答は正解


class QuestionSerializerTest(TestCase):
    """
    QuestionSerializerのテスト
    """
    
    def setUp(self):
        """
        テスト前の準備
        """
        # カテゴリーと難易度を作成
        self.category = Category.objects.create(
            name='Python基礎',
            slug='python-basics'
        )
        self.difficulty = DifficultyLevel.objects.create(
            name='初級',
            slug='beginner',
            level=1
        )
        
        # クイズを作成
        self.quiz = Quiz.objects.create(
            category=self.category,
            difficulty=self.difficulty,
            title='Python変数と型'
        )
        
        # 問題を作成
        self.question_attributes = {
            'quiz': self.quiz,
            'question_text': 'Pythonリストの特徴は？',
            'question_type': 'multiple_choice',
            'hint': 'データの順序と変更可能性を考えてください',
            'explanation': 'リストは順序付けられた変更可能なコレクションです',
            'points': 15,
            'display_order': 1,
            'code_snippet': 'my_list = [1, 2, 3]',
            'media_type': 'code',
            'syntax_highlight': 'python'
        }
        self.question = Question.objects.create(**self.question_attributes)
        
        # 回答を作成
        self.answer1 = Answer.objects.create(
            question=self.question,
            answer_text="順序付けられている",
            is_correct=True,
            display_order=1
        )
        self.answer2 = Answer.objects.create(
            question=self.question,
            answer_text="変更可能",
            is_correct=True,
            display_order=2
        )
        self.answer3 = Answer.objects.create(
            question=self.question,
            answer_text="キーと値のペア",
            is_correct=False,
            display_order=3
        )
        
        self.serializer = QuestionSerializer(instance=self.question)

    def test_contains_expected_fields(self):
        """
        シリアライザーが期待されるフィールドを含んでいるかテスト
        """
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set([
            'id', 'quiz', 'question_text', 'question_type', 
            'hint', 'explanation', 'points', 'display_order', 
            'code_snippet', 'image_url', 'media_type', 
            'syntax_highlight', 'answers', 'created_at', 'updated_at'
        ]))

    def test_field_content(self):
        """
        各フィールドの内容が正しいかテスト
        """
        data = self.serializer.data
        self.assertEqual(data['question_text'], self.question_attributes['question_text'])
        self.assertEqual(data['question_type'], self.question_attributes['question_type'])
        self.assertEqual(data['hint'], self.question_attributes['hint'])
        self.assertEqual(data['explanation'], self.question_attributes['explanation'])
        self.assertEqual(data['points'], self.question_attributes['points'])
        self.assertEqual(data['code_snippet'], self.question_attributes['code_snippet'])
        self.assertEqual(data['media_type'], self.question_attributes['media_type'])
        self.assertEqual(data['syntax_highlight'], self.question_attributes['syntax_highlight'])

    def test_answers_are_included(self):
        """
        回答が正しく含まれているかテスト
        """
        data = self.serializer.data
        # 回答の数が正しいか確認
        self.assertEqual(len(data['answers']), 3)
        
        # 回答の内容をチェック
        answer1_data = next(a for a in data['answers'] if a['display_order'] == 1)
        answer2_data = next(a for a in data['answers'] if a['display_order'] == 2)
        answer3_data = next(a for a in data['answers'] if a['display_order'] == 3)
        
        self.assertEqual(answer1_data['answer_text'], self.answer1.answer_text)
        self.assertTrue(answer1_data['is_correct'])
        
        self.assertEqual(answer2_data['answer_text'], self.answer2.answer_text)
        self.assertTrue(answer2_data['is_correct'])
        
        self.assertEqual(answer3_data['answer_text'], self.answer3.answer_text)
        self.assertFalse(answer3_data['is_correct'])

    def test_deserialization_valid_data(self):
        """
        有効なデータでデシリアライズできるかテスト
        """
        valid_serializer_data = {
            'quiz': self.quiz.id,
            'question_text': '新しい問題',
            'question_type': 'true_false',
            'hint': 'ヒント',
            'explanation': '解説',
            'points': 10,
            'display_order': 2
        }
        serializer = QuestionSerializer(data=valid_serializer_data)
        self.assertTrue(serializer.is_valid())
        new_question = serializer.save()
        self.assertEqual(new_question.question_text, valid_serializer_data['question_text'])
        self.assertEqual(new_question.quiz.id, valid_serializer_data['quiz'])


class AnswerSerializerTest(TestCase):
    """
    AnswerSerializerのテスト
    """
    
    def setUp(self):
        """
        テスト前の準備
        """
        # カテゴリー、難易度、クイズ、問題を作成
        self.category = Category.objects.create(name='カテゴリ', slug='category')
        self.difficulty = DifficultyLevel.objects.create(name='難易度', slug='level', level=1)
        self.quiz = Quiz.objects.create(
            category=self.category,
            difficulty=self.difficulty,
            title='クイズ'
        )
        self.question = Question.objects.create(
            quiz=self.quiz,
            question_text='問題',
            question_type='single_choice'
        )
        
        # 回答を作成
        self.answer_attributes = {
            'question': self.question,
            'answer_text': '回答テキスト',
            'is_correct': True,
            'feedback': '正解です！',
            'display_order': 1
        }
        self.answer = Answer.objects.create(**self.answer_attributes)
        self.serializer = AnswerSerializer(instance=self.answer)

    def test_contains_expected_fields(self):
        """
        シリアライザーが期待されるフィールドを含んでいるかテスト
        """
        data = self.serializer.data
        self.assertEqual(set(data.keys()), set([
            'id', 'question', 'answer_text', 'is_correct', 
            'feedback', 'display_order', 'created_at', 'updated_at'
        ]))

    def test_field_content(self):
        """
        各フィールドの内容が正しいかテスト
        """
        data = self.serializer.data
        self.assertEqual(data['answer_text'], self.answer_attributes['answer_text'])
        self.assertEqual(data['is_correct'], self.answer_attributes['is_correct'])
        self.assertEqual(data['feedback'], self.answer_attributes['feedback'])
        self.assertEqual(data['display_order'], self.answer_attributes['display_order'])
        self.assertEqual(data['question'], self.question.id)

    def test_deserialization_valid_data(self):
        """
        有効なデータでデシリアライズできるかテスト
        """
        valid_serializer_data = {
            'question': self.question.id,
            'answer_text': '新しい回答',
            'is_correct': False,
            'feedback': '不正解です',
            'display_order': 2
        }
        serializer = AnswerSerializer(data=valid_serializer_data)
        self.assertTrue(serializer.is_valid())
        new_answer = serializer.save()
        self.assertEqual(new_answer.answer_text, valid_serializer_data['answer_text'])
        self.assertEqual(new_answer.is_correct, valid_serializer_data['is_correct'])
        self.assertEqual(new_answer.question.id, valid_serializer_data['question'])


# Quiz結果と統計情報、活動履歴のテストには認証ユーザーが必要
User = get_user_model()

class QuizResultSerializerTest(TestCase):
    """
    QuizResultSerializerのテスト
    """
    
    def setUp(self):
        """
        テスト前の準備
        """
        # ユーザー、カテゴリー、難易度、クイズを作成
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password'
        )
        self.category = Category.objects.create(name='カテゴリ', slug='category')
        self.difficulty = DifficultyLevel.objects.create(name='難易度', slug='level', level=1)
        self.quiz = Quiz.objects.create(
            category=self.category,
            difficulty=self.difficulty,
            title='クイズ',
            pass_score=70
        )
        
        # クイズ結果を作成
        self.result_attributes = {
            'user': self.user,
            'quiz': self.quiz,
            'score': 80,
            'total_possible': 100,
            'percentage': 80.0,
            'time_taken': 300,
            'passed': True
        }
        self.result = QuizResult.objects.create(**self.result_attributes)
        self.serializer = QuizResultSerializer(instance=self.result)

    def test_contains_expected_fields(self):
        """
        シリアライザーが期待されるフィールドを含んでいるかテスト
        """
        data = self.serializer.data
        expected_fields = set([
            'id', 'user', 'username', 'quiz', 'quiz_title', 
            'category_name', 'difficulty_name', 
            'score', 'total_possible', 'percentage', 
            'time_taken', 'passed', 'completed_at', 
            'created_at', 'updated_at'
        ])
        self.assertEqual(set(data.keys()), expected_fields)

    def test_field_content(self):
        """
        各フィールドの内容が正しいかテスト
        """
        data = self.serializer.data
        self.assertEqual(data['user'], self.user.id)
        self.assertEqual(data['username'], self.user.username)
        self.assertEqual(data['quiz'], self.quiz.id)
        self.assertEqual(data['quiz_title'], self.quiz.title)
        self.assertEqual(data['category_name'], self.category.name)
        self.assertEqual(data['difficulty_name'], self.difficulty.name)
        self.assertEqual(data['score'], self.result_attributes['score'])
        self.assertEqual(data['total_possible'], self.result_attributes['total_possible'])
        self.assertEqual(data['percentage'], self.result_attributes['percentage'])
        self.assertEqual(data['time_taken'], self.result_attributes['time_taken'])
        self.assertEqual(data['passed'], self.result_attributes['passed'])

    def test_deserialization_valid_data(self):
        """
        有効なデータでデシリアライズできるかテスト
        """
        # userフィールドはread_onlyなので含めない
        valid_serializer_data = {
            'quiz': self.quiz.id,
            'score': 60,
            'total_possible': 100,
            'percentage': 60.0,
            'time_taken': 400
        }
        serializer = QuizResultSerializer(data=valid_serializer_data)
        self.assertTrue(serializer.is_valid())
        
        # saveの際にuserを明示的に設定
        new_result = serializer.save(user=self.user)
        
        # 保存されたデータを検証
        self.assertEqual(new_result.user.id, self.user.id)
        self.assertEqual(new_result.quiz.id, self.quiz.id)
        # passedフィールドは自動的に設定される
        self.assertFalse(new_result.passed)  # 60点は70点以下なので不合格


class UserStatisticsSerializerTest(TestCase):
    """
    UserStatisticsSerializerのテスト
    """
    
    def setUp(self):
        """
        テスト前の準備
        """
        # 必要なインポート
        from django.utils import timezone
        
        # ユーザー、カテゴリー、難易度を作成
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password'
        )
        self.category = Category.objects.create(name='カテゴリ', slug='category')
        self.difficulty = DifficultyLevel.objects.create(name='難易度', slug='level', level=1)
        
        # 統計情報を作成
        self.stats_attributes = {
            'user': self.user,
            'category': self.category,
            'difficulty': self.difficulty,
            'quizzes_completed': 5,
            'total_points': 400,
            'avg_score': 80.0,
            'highest_score': 95,
            'last_quiz_date': timezone.now()
        }
        self.stats = UserStatistics.objects.create(**self.stats_attributes)
        self.serializer = UserStatisticsSerializer(instance=self.stats)

    def test_contains_expected_fields(self):
        """
        シリアライザーが期待されるフィールドを含んでいるかテスト
        """
        data = self.serializer.data
        expected_fields = set([
            'id', 'user', 'username', 'category', 'category_name', 
            'difficulty', 'difficulty_name', 'quizzes_completed', 
            'total_points', 'avg_score', 'highest_score', 
            'last_quiz_date', 'created_at', 'updated_at'
        ])
        self.assertEqual(set(data.keys()), expected_fields)

    def test_field_content(self):
        """
        各フィールドの内容が正しいかテスト
        """
        data = self.serializer.data
        self.assertEqual(data['user'], self.user.id)
        self.assertEqual(data['username'], self.user.username)
        self.assertEqual(data['category'], self.category.id)
        self.assertEqual(data['category_name'], self.category.name)
        self.assertEqual(data['difficulty'], self.difficulty.id)
        self.assertEqual(data['difficulty_name'], self.difficulty.name)
        self.assertEqual(data['quizzes_completed'], self.stats_attributes['quizzes_completed'])
        self.assertEqual(data['total_points'], self.stats_attributes['total_points'])
        self.assertEqual(data['avg_score'], self.stats_attributes['avg_score'])
        self.assertEqual(data['highest_score'], self.stats_attributes['highest_score'])

    def test_null_difficulty_name(self):
        """
        difficultyがNullの場合のdifficulty_name取得をテスト
        """
        # 難易度なしの統計を作成
        no_difficulty_stats = UserStatistics.objects.create(
            user=self.user,
            category=self.category,
            difficulty=None,
            quizzes_completed=3,
            total_points=240,
            avg_score=80.0
        )
        serializer = UserStatisticsSerializer(instance=no_difficulty_stats)
        self.assertEqual(serializer.data['difficulty_name'], "全難易度")


class ActivityHistorySerializerTest(TestCase):
    """
    ActivityHistorySerializerのテスト
    """
    
    def setUp(self):
        """
        テスト前の準備
        """
        # ユーザー、カテゴリー、難易度、クイズを作成
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='password'
        )
        self.category = Category.objects.create(name='カテゴリ', slug='category')
        self.difficulty = DifficultyLevel.objects.create(name='難易度', slug='level', level=1)
        self.quiz = Quiz.objects.create(
            category=self.category,
            difficulty=self.difficulty,
            title='クイズ'
        )
        
        # 活動履歴を作成
        self.activity_attributes = {
            'user': self.user,
            'quiz': self.quiz,
            'category': self.category,
            'difficulty': self.difficulty,
            'score': 85,
            'percentage': 85.0,
            'activity_type': 'quiz_completed'
        }
        self.activity = ActivityHistory.objects.create(**self.activity_attributes)
        self.serializer = ActivityHistorySerializer(instance=self.activity)

    def test_contains_expected_fields(self):
        """
        シリアライザーが期待されるフィールドを含んでいるかテスト
        """
        data = self.serializer.data
        expected_fields = set([
            'id', 'user', 'username', 'quiz', 'quiz_title', 
            'category', 'category_name', 'difficulty', 'difficulty_name', 
            'score', 'percentage', 'activity_date', 
            'activity_type', 'activity_type_display',
            'created_at', 'updated_at'
        ])
        self.assertEqual(set(data.keys()), expected_fields)

    def test_field_content(self):
        """
        各フィールドの内容が正しいかテスト
        """
        data = self.serializer.data
        self.assertEqual(data['user'], self.user.id)
        self.assertEqual(data['username'], self.user.username)
        self.assertEqual(data['quiz'], self.quiz.id)
        self.assertEqual(data['quiz_title'], self.quiz.title)
        self.assertEqual(data['category'], self.category.id)
        self.assertEqual(data['category_name'], self.category.name)
        self.assertEqual(data['difficulty'], self.difficulty.id)
        self.assertEqual(data['difficulty_name'], self.difficulty.name)
        self.assertEqual(data['score'], self.activity_attributes['score'])
        self.assertEqual(data['percentage'], self.activity_attributes['percentage'])
        self.assertEqual(data['activity_type'], self.activity_attributes['activity_type'])
        self.assertEqual(data['activity_type_display'], 'クイズ完了')  # get_activity_type_display

    def test_deserialization_valid_data(self):
        """
        有効なデータでデシリアライズできるかテスト
        """
        valid_serializer_data = {
            'user': self.user.id,
            'quiz': self.quiz.id,
            'category': self.category.id,
            'difficulty': self.difficulty.id,
            'score': 70,
            'percentage': 70.0,
            'activity_type': 'quiz_review'
        }
        serializer = ActivityHistorySerializer(data=valid_serializer_data)
        self.assertTrue(serializer.is_valid())
        new_activity = serializer.save()
        self.assertEqual(new_activity.score, valid_serializer_data['score'])
        self.assertEqual(new_activity.activity_type, valid_serializer_data['activity_type'])
        self.assertEqual(new_activity.user.id, valid_serializer_data['user'])
        self.assertEqual(new_activity.quiz.id, valid_serializer_data['quiz']) 