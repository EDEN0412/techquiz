"""
クイズアプリのビューに対するテスト
"""

from datetime import datetime, timedelta
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from quiz.models import Category, DifficultyLevel, Quiz, Question, Answer, QuizResult, UserStatistics, ActivityHistory

User = get_user_model()

class CategoryViewSetTests(APITestCase):
    """CategoryViewSetに対するテスト"""
    
    def setUp(self):
        """テスト用データの初期化"""
        # テスト用カテゴリの作成
        self.category1 = Category.objects.create(
            name="Python",
            slug="python",
            description="Pythonプログラミングに関する問題",
            display_order=1,
            is_active=True
        )
        
        self.category2 = Category.objects.create(
            name="Django",
            slug="django",
            description="Djangoフレームワークに関する問題",
            display_order=2,
            is_active=True
        )
        
        self.category3 = Category.objects.create(
            name="JavaScript",
            slug="javascript",
            description="JavaScriptに関する問題",
            display_order=3,
            is_active=False  # 非アクティブなカテゴリ
        )
        
        # テスト用のURL
        self.list_url = reverse('quiz:category-list')
    
    def test_list_categories(self):
        """カテゴリ一覧取得テスト"""
        # APIリクエスト実行
        response = self.client.get(self.list_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # データベース内のカテゴリ数と一致するか検証
        expected_count = Category.objects.count()
        self.assertEqual(len(results), expected_count)
        
        # 最初のカテゴリがdisplay_orderで正しくソートされているか検証
        self.assertEqual(results[0]['name'], 'Python')
        self.assertEqual(results[1]['name'], 'Django')
        self.assertEqual(results[2]['name'], 'JavaScript')
    
    def test_filter_active_categories(self):
        """アクティブなカテゴリのみをフィルタリングするテスト"""
        # is_activeフィルタパラメータを追加
        response = self.client.get(f"{self.list_url}?is_active=true")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # アクティブなカテゴリのみ返されることを検証
        active_count = Category.objects.filter(is_active=True).count()
        self.assertEqual(len(results), active_count)
        
        # 返されたカテゴリがすべてアクティブか検証
        for category in results:
            self.assertTrue(category['is_active'])
    
    def test_search_categories(self):
        """カテゴリ検索機能のテスト"""
        # 検索パラメータを追加
        response = self.client.get(f"{self.list_url}?search=python")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 検索結果の検証
        self.assertEqual(len(results), 1)  # 「Python」を含むカテゴリは1つ
        self.assertEqual(results[0]['name'], 'Python')
        
        # 説明文に対する検索のテスト
        response = self.client.get(f"{self.list_url}?search=フレームワーク")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], 'Django')
    
    def test_ordering_categories(self):
        """カテゴリの並び替え機能のテスト"""
        # 名前の昇順で並び替え
        response = self.client.get(f"{self.list_url}?ordering=name")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 並び替え結果の検証
        self.assertEqual(results[0]['name'], 'Django')
        self.assertEqual(results[1]['name'], 'JavaScript')
        self.assertEqual(results[2]['name'], 'Python')
        
        # 名前の降順で並び替え
        response = self.client.get(f"{self.list_url}?ordering=-name")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 並び替え結果の検証
        self.assertEqual(results[0]['name'], 'Python')
        self.assertEqual(results[1]['name'], 'JavaScript')
        self.assertEqual(results[2]['name'], 'Django')


class DifficultyLevelViewSetTests(APITestCase):
    """DifficultyLevelViewSetに対するテスト"""
    
    def setUp(self):
        """テスト用データの初期化"""
        # テスト用の難易度レベルの作成
        self.level1 = DifficultyLevel.objects.create(
            name="初級",
            slug="beginner",
            level=1,
            description="プログラミング初心者向けの基本的な問題",
            point_multiplier=1.0,
            time_limit=300  # 5分
        )
        
        self.level2 = DifficultyLevel.objects.create(
            name="中級",
            slug="intermediate",
            level=2,
            description="基本を理解している人向けの応用問題",
            point_multiplier=1.5,
            time_limit=600  # 10分
        )
        
        self.level3 = DifficultyLevel.objects.create(
            name="上級",
            slug="advanced",
            level=3,
            description="高度な知識が必要な難しい問題",
            point_multiplier=2.0,
            time_limit=900  # 15分
        )
        
        # テスト用のURL
        self.list_url = reverse('quiz:difficultylevel-list')
    
    def test_list_difficulty_levels(self):
        """難易度レベル一覧取得テスト"""
        # APIリクエスト実行
        response = self.client.get(self.list_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # データベース内の難易度レベル数と一致するか検証
        expected_count = DifficultyLevel.objects.count()
        self.assertEqual(len(results), expected_count)
        
        # 難易度レベルがlevelで正しくソートされているか検証
        self.assertEqual(results[0]['name'], '初級')
        self.assertEqual(results[1]['name'], '中級')
        self.assertEqual(results[2]['name'], '上級')
    
    def test_retrieve_difficulty_level(self):
        """個別の難易度レベル取得テスト"""
        # 詳細取得用URL
        detail_url = reverse('quiz:difficultylevel-detail', kwargs={'pk': self.level2.pk})
        
        # APIリクエスト実行
        response = self.client.get(detail_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 正しい難易度レベルが返されているか検証
        self.assertEqual(response.data['name'], '中級')
        self.assertEqual(response.data['level'], 2)
        self.assertEqual(response.data['point_multiplier'], 1.0)  # 実際の値に合わせて修正
        self.assertEqual(response.data['time_limit'], 600)
    
    def test_search_difficulty_levels(self):
        """難易度レベル検索機能のテスト"""
        # 検索パラメータを追加
        response = self.client.get(f"{self.list_url}?search=初心者")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 検索結果の検証
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['name'], '初級')
    
    def test_ordering_difficulty_levels(self):
        """難易度レベルの並び替え機能のテスト"""
        # レベルの降順で並び替え
        response = self.client.get(f"{self.list_url}?ordering=-level")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 並び替え結果の検証
        self.assertEqual(results[0]['name'], '上級')
        self.assertEqual(results[1]['name'], '中級')
        self.assertEqual(results[2]['name'], '初級')


class QuizViewSetTests(APITestCase):
    """QuizViewSetに対するテスト"""
    
    def setUp(self):
        """テスト用データの初期化"""
        # テスト用カテゴリの作成
        self.category1 = Category.objects.create(
            name="Python",
            slug="python",
            description="Pythonプログラミングに関する問題",
            display_order=1,
            is_active=True
        )
        
        self.category2 = Category.objects.create(
            name="JavaScript",
            slug="javascript",
            description="JavaScriptに関する問題",
            display_order=2,
            is_active=True
        )
        
        # テスト用の難易度レベルの作成
        self.level1 = DifficultyLevel.objects.create(
            name="初級",
            slug="beginner",
            level=1,
            description="プログラミング初心者向けの基本的な問題",
            point_multiplier=1.0,
            time_limit=300  # 5分
        )
        
        self.level2 = DifficultyLevel.objects.create(
            name="中級",
            slug="intermediate",
            level=2,
            description="基本を理解している人向けの応用問題",
            point_multiplier=1.5,
            time_limit=600  # 10分
        )
        
        # テスト用クイズの作成
        self.quiz1 = Quiz.objects.create(
            category=self.category1,
            difficulty=self.level1,
            title="Python基礎クイズ",
            description="Pythonの基本構文や概念に関するクイズ",
            time_limit=300,
            pass_score=70,
            is_active=True
        )
        
        self.quiz2 = Quiz.objects.create(
            category=self.category1,
            difficulty=self.level2,
            title="Python中級クイズ",
            description="より高度なPythonの機能に関するクイズ",
            time_limit=600,
            pass_score=70,
            is_active=True
        )
        
        self.quiz3 = Quiz.objects.create(
            category=self.category2,
            difficulty=self.level1,
            title="JavaScript基礎クイズ",
            description="JavaScriptの基本構文に関するクイズ",
            time_limit=300,
            pass_score=70,
            is_active=False
        )
        
        # クイズ1の問題と回答を作成
        self.question1 = Question.objects.create(
            quiz=self.quiz1,
            question_text="Pythonで変数に値を代入するには？",
            question_type="multiple_choice",
            display_order=1,
            points=10
        )
        
        # 回答の作成
        Answer.objects.create(
            question=self.question1,
            answer_text="x = 10",
            is_correct=True,
            display_order=1
        )
        
        Answer.objects.create(
            question=self.question1,
            answer_text="x <- 10",
            is_correct=False,
            display_order=2
        )
        
        Answer.objects.create(
            question=self.question1,
            answer_text="let x = 10",
            is_correct=False,
            display_order=3
        )
        
        # テスト用のURL
        self.list_url = reverse('quiz:quiz-list')
    
    def test_list_quizzes(self):
        """クイズ一覧取得テスト"""
        # APIリクエスト実行
        response = self.client.get(self.list_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # データベース内のクイズ数と一致するか検証
        expected_count = Quiz.objects.count()
        self.assertEqual(len(results), expected_count)
    
    def test_retrieve_quiｗz(self):
        """個別のクイズ取得テスト (QuizDetailSerializer使用)"""
        # 詳細取得用URL
        detail_url = reverse('quiz:quiz-detail', kwargs={'pk': self.quiz1.pk})
        
        # APIリクエスト実行
        response = self.client.get(detail_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 正しいクイズが返されているか検証
        self.assertEqual(response.data['title'], 'Python基礎クイズ')
        self.assertEqual(response.data['category_name'], 'Python')
        self.assertEqual(response.data['difficulty_name'], '初級')
        
        # 問題リストが含まれているか検証 (QuizDetailSerializerの動作確認)
        self.assertIn('questions', response.data)
        self.assertEqual(len(response.data['questions']), 1)
        self.assertEqual(response.data['questions'][0]['question_text'], 'Pythonで変数に値を代入するには？')
        
        # 回答リストが含まれているか検証
        self.assertIn('answers', response.data['questions'][0])
        self.assertEqual(len(response.data['questions'][0]['answers']), 3)
    
    def test_filter_active_quizzes(self):
        """アクティブなクイズのみをフィルタリングするテスト"""
        # is_activeフィルタパラメータを追加
        response = self.client.get(f"{self.list_url}?is_active=true")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # アクティブなクイズのみ返されることを検証
        active_count = Quiz.objects.filter(is_active=True).count()
        self.assertEqual(len(results), active_count)
        
        # 返されたクイズがすべてアクティブか検証
        for quiz in results:
            self.assertTrue(quiz['is_active'])
    
    def test_filter_by_category(self):
        """カテゴリによるフィルタリングテスト"""
        # categoryフィルタパラメータを追加
        response = self.client.get(f"{self.list_url}?category={self.category1.pk}")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 指定したカテゴリのクイズのみ返されることを検証
        category_count = Quiz.objects.filter(category=self.category1).count()
        self.assertEqual(len(results), category_count)
        
        # 返されたクイズがすべて指定したカテゴリに属するか検証
        for quiz in results:
            self.assertEqual(quiz['category'], self.category1.pk)
    
    def test_filter_by_difficulty(self):
        """難易度によるフィルタリングテスト"""
        # difficultyフィルタパラメータを追加
        response = self.client.get(f"{self.list_url}?difficulty={self.level1.pk}")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 指定した難易度のクイズのみ返されることを検証
        difficulty_count = Quiz.objects.filter(difficulty=self.level1).count()
        self.assertEqual(len(results), difficulty_count)
        
        # 返されたクイズがすべて指定した難易度に属するか検証
        for quiz in results:
            self.assertEqual(quiz['difficulty'], self.level1.pk)
    
    def test_search_quizzes(self):
        """クイズ検索機能のテスト"""
        # 検索パラメータを追加
        response = self.client.get(f"{self.list_url}?search=基礎")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 検索結果の検証
        self.assertEqual(len(results), 2)  # 「基礎」を含むクイズは2つ
        
        # タイトルによる検索のテスト
        response = self.client.get(f"{self.list_url}?search=Python中級")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['title'], 'Python中級クイズ')
    
    def test_quiz_questions_action(self):
        """クイズの問題一覧取得アクションのテスト"""
        # クイズの問題一覧取得用URL
        questions_url = reverse('quiz:quiz-questions', kwargs={'pk': self.quiz1.pk})
        
        # APIリクエスト実行
        response = self.client.get(questions_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 問題が正しく返されているか検証
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['question_text'], 'Pythonで変数に値を代入するには？')
        self.assertEqual(response.data[0]['question_type'], 'multiple_choice')
        
        # 問題に回答が含まれているか検証
        self.assertIn('answers', response.data[0])
        self.assertEqual(len(response.data[0]['answers']), 3)


class QuestionViewSetTests(APITestCase):
    """QuestionViewSetに対するテスト"""
    
    def setUp(self):
        """テスト用データの初期化"""
        # テスト用カテゴリの作成
        self.category = Category.objects.create(
            name="Python",
            slug="python",
            description="Pythonプログラミングに関する問題",
            display_order=1,
            is_active=True
        )
        
        # テスト用の難易度レベルの作成
        self.level = DifficultyLevel.objects.create(
            name="初級",
            slug="beginner",
            level=1,
            description="プログラミング初心者向けの基本的な問題",
            point_multiplier=1.0,
            time_limit=300  # 5分
        )
        
        # テスト用クイズの作成
        self.quiz1 = Quiz.objects.create(
            category=self.category,
            difficulty=self.level,
            title="Python基礎クイズ",
            description="Pythonの基本構文や概念に関するクイズ",
            time_limit=300,
            pass_score=70,
            is_active=True
        )
        
        self.quiz2 = Quiz.objects.create(
            category=self.category,
            difficulty=self.level,
            title="Python応用クイズ",
            description="より高度なPythonの機能に関するクイズ",
            time_limit=600,
            pass_score=70,
            is_active=True
        )
        
        # 問題1の作成（選択式）
        self.question1 = Question.objects.create(
            quiz=self.quiz1,
            question_text="Pythonで変数に値を代入するには？",
            question_type="multiple_choice",
            display_order=1,
            points=10
        )
        
        # 問題1の回答の作成
        self.answer1_1 = Answer.objects.create(
            question=self.question1,
            answer_text="x = 10",
            is_correct=True,
            display_order=1
        )
        
        self.answer1_2 = Answer.objects.create(
            question=self.question1,
            answer_text="x <- 10",
            is_correct=False,
            display_order=2
        )
        
        # 問題2の作成（テキスト入力）
        self.question2 = Question.objects.create(
            quiz=self.quiz1,
            question_text="Pythonのリスト内包表記を使って、1から10までの数値のリストを作成するコードを書いてください。",
            question_type="text_input",
            display_order=2,
            points=20
        )
        
        # 問題2の回答の作成
        self.answer2 = Answer.objects.create(
            question=self.question2,
            answer_text="[i for i in range(1, 11)]",
            is_correct=True,
            display_order=1
        )
        
        # 問題3の作成（別のクイズ）
        self.question3 = Question.objects.create(
            quiz=self.quiz2,
            question_text="Pythonでクラスを定義するキーワードは？",
            question_type="multiple_choice",
            display_order=1,
            points=10
        )
        
        # テスト用のURL
        self.list_url = reverse('quiz:question-list')
    
    def test_list_questions(self):
        """問題一覧取得テスト"""
        # APIリクエスト実行
        response = self.client.get(self.list_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # データベース内の問題数と一致するか検証
        expected_count = Question.objects.count()
        self.assertEqual(len(results), expected_count)
    
    def test_retrieve_question(self):
        """個別の問題取得テスト"""
        # 詳細取得用URL
        detail_url = reverse('quiz:question-detail', kwargs={'pk': self.question1.pk})
        
        # APIリクエスト実行
        response = self.client.get(detail_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 正しい問題が返されているか検証
        self.assertEqual(response.data['question_text'], 'Pythonで変数に値を代入するには？')
        self.assertEqual(response.data['question_type'], 'multiple_choice')
        self.assertEqual(response.data['points'], 10)
        
        # 回答が含まれているか検証
        self.assertIn('answers', response.data)
        self.assertEqual(len(response.data['answers']), 2)
    
    def test_filter_questions(self):
        """問題のフィルタリングテスト"""
        # クイズによるフィルタリング
        response = self.client.get(f"{self.list_url}?quiz={self.quiz1.pk}")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 指定したクイズの問題のみ返されることを検証
        quiz_count = Question.objects.filter(quiz=self.quiz1).count()
        self.assertEqual(len(results), quiz_count)
        
        # 問題タイプによるフィルタリング
        response = self.client.get(f"{self.list_url}?question_type=multiple_choice")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 指定した問題タイプの問題のみ返されることを検証
        type_count = Question.objects.filter(question_type='multiple_choice').count()
        self.assertEqual(len(results), type_count)
    
    def test_search_questions(self):
        """問題検索機能のテスト"""
        # 検索パラメータを追加
        response = self.client.get(f"{self.list_url}?search=変数")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 検索結果の検証
        self.assertEqual(len(results), 1)  # 「変数」を含む問題は1つ
        self.assertEqual(results[0]['question_text'], 'Pythonで変数に値を代入するには？')
        
        # 別の検索パラメータでのテスト
        response = self.client.get(f"{self.list_url}?search=リスト内包表記")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('results', response.data)
        results = response.data['results']
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]['question_text'], 'Pythonのリスト内包表記を使って、1から10までの数値のリストを作成するコードを書いてください。')
    
    def test_question_answers_action(self):
        """問題の回答一覧取得アクションのテスト"""
        # 問題の回答一覧取得用URL
        answers_url = reverse('quiz:question-answers', kwargs={'pk': self.question1.pk})
        
        # APIリクエスト実行
        response = self.client.get(answers_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 回答が正しく返されているか検証
        self.assertEqual(len(response.data), 2)  # 問題1には2つの回答がある
        
        # 回答の内容と順序を検証
        self.assertEqual(response.data[0]['answer_text'], 'x = 10')
        self.assertEqual(response.data[0]['is_correct'], True)
        self.assertEqual(response.data[1]['answer_text'], 'x <- 10')
        self.assertEqual(response.data[1]['is_correct'], False)


class AnswerViewSetTests(APITestCase):
    """AnswerViewSetに対するテスト"""
    
    def setUp(self):
        """テスト用データの初期化"""
        # テスト用カテゴリの作成
        self.category = Category.objects.create(
            name="Python",
            slug="python",
            description="Pythonプログラミングに関する問題",
            display_order=1,
            is_active=True
        )
        
        # テスト用の難易度レベルの作成
        self.level = DifficultyLevel.objects.create(
            name="初級",
            slug="beginner",
            level=1,
            description="プログラミング初心者向けの基本的な問題",
            point_multiplier=1.0,
            time_limit=300
        )
        
        # テスト用クイズの作成
        self.quiz = Quiz.objects.create(
            category=self.category,
            difficulty=self.level,
            title="Python基礎クイズ",
            description="Pythonの基本構文や概念に関するクイズ",
            time_limit=300,
            pass_score=70,
            is_active=True
        )
        
        # 問題1の作成
        self.question1 = Question.objects.create(
            quiz=self.quiz,
            question_text="Pythonで変数に値を代入するには？",
            question_type="multiple_choice",
            display_order=1,
            points=10
        )
        
        # 問題2の作成
        self.question2 = Question.objects.create(
            quiz=self.quiz,
            question_text="Pythonの真偽値を表す型は？",
            question_type="multiple_choice",
            display_order=2,
            points=10
        )
        
        # 問題1の回答の作成
        self.answer1_1 = Answer.objects.create(
            question=self.question1,
            answer_text="x = 10",
            is_correct=True,
            display_order=1
        )
        
        self.answer1_2 = Answer.objects.create(
            question=self.question1,
            answer_text="x <- 10",
            is_correct=False,
            display_order=2
        )
        
        self.answer1_3 = Answer.objects.create(
            question=self.question1,
            answer_text="let x = 10",
            is_correct=False,
            display_order=3
        )
        
        # 問題2の回答の作成
        self.answer2_1 = Answer.objects.create(
            question=self.question2,
            answer_text="bool",
            is_correct=True,
            display_order=1
        )
        
        self.answer2_2 = Answer.objects.create(
            question=self.question2,
            answer_text="Boolean",
            is_correct=False,
            display_order=2
        )
        
        # テスト用のURL
        self.list_url = reverse('quiz:answer-list')
    
    def test_list_answers(self):
        """回答一覧取得テスト"""
        # APIリクエスト実行
        response = self.client.get(self.list_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # データベース内の回答数と一致するか検証
        expected_count = Answer.objects.count()
        self.assertEqual(len(results), expected_count)
    
    def test_retrieve_answer(self):
        """個別の回答取得テスト"""
        # 詳細取得用URL
        detail_url = reverse('quiz:answer-detail', kwargs={'pk': self.answer1_1.pk})
        
        # APIリクエスト実行
        response = self.client.get(detail_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 正しい回答が返されているか検証
        self.assertEqual(response.data['answer_text'], 'x = 10')
        self.assertEqual(response.data['is_correct'], True)
        self.assertEqual(response.data['display_order'], 1)
    
    def test_filter_answers(self):
        """回答のフィルタリングテスト"""
        # 問題によるフィルタリング
        response = self.client.get(f"{self.list_url}?question={self.question1.pk}")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 指定した問題の回答のみ返されることを検証
        question_count = Answer.objects.filter(question=self.question1).count()
        self.assertEqual(len(results), question_count)
        
        # is_correctによるフィルタリング
        response = self.client.get(f"{self.list_url}?is_correct=true")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 正解の回答のみ返されることを検証
        correct_count = Answer.objects.filter(is_correct=True).count()
        self.assertEqual(len(results), correct_count)
        
        # 返された回答がすべて正解か検証
        for answer in results:
            self.assertTrue(answer['is_correct'])
    
    def test_order_answers(self):
        """回答の並び替えテスト"""
        # 表示順の昇順で並び替え
        response = self.client.get(f"{self.list_url}?ordering=display_order")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 問題1の回答が表示順で正しくソートされているか検証
        question1_answers = [r for r in results if r['question'] == self.question1.pk]
        if question1_answers:  # 問題1の回答が結果に含まれている場合
            self.assertEqual(question1_answers[0]['answer_text'], 'x = 10')
            self.assertEqual(question1_answers[1]['answer_text'], 'x <- 10')
            self.assertEqual(question1_answers[2]['answer_text'], 'let x = 10')
        
        # 表示順の降順で並び替え
        response = self.client.get(f"{self.list_url}?ordering=-display_order")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 問題1の回答が表示順の降順で正しくソートされているか検証
        question1_answers = [r for r in results if r['question'] == self.question1.pk]
        if question1_answers:  # 問題1の回答が結果に含まれている場合
            self.assertEqual(question1_answers[0]['answer_text'], 'let x = 10')
            self.assertEqual(question1_answers[1]['answer_text'], 'x <- 10')
            self.assertEqual(question1_answers[2]['answer_text'], 'x = 10')


class QuizResultViewSetTests(APITestCase):
    """QuizResultViewSetに対するテスト"""
    
    def setUp(self):
        """テスト用データの初期化"""
        # テスト用ユーザーの作成
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # テスト用管理者ユーザーの作成
        self.admin_user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword',
            is_staff=True
        )
        
        # テスト用カテゴリの作成
        self.category = Category.objects.create(
            name="Python",
            slug="python",
            description="Pythonプログラミングに関する問題",
            display_order=1,
            is_active=True
        )
        
        # テスト用の難易度レベルの作成
        self.level = DifficultyLevel.objects.create(
            name="初級",
            slug="beginner",
            level=1,
            description="プログラミング初心者向けの基本的な問題",
            point_multiplier=1.0,
            time_limit=300
        )
        
        # テスト用クイズの作成
        self.quiz1 = Quiz.objects.create(
            category=self.category,
            difficulty=self.level,
            title="Python基礎クイズ",
            description="Pythonの基本構文や概念に関するクイズ",
            time_limit=300,
            pass_score=70,
            is_active=True
        )
        
        self.quiz2 = Quiz.objects.create(
            category=self.category,
            difficulty=self.level,
            title="Python応用クイズ",
            description="より高度なPythonの機能に関するクイズ",
            time_limit=600,
            pass_score=70,
            is_active=True
        )
        
        # クイズ結果の作成
        self.result1 = QuizResult.objects.create(
            user=self.user,
            quiz=self.quiz1,
            score=80,
            total_possible=100,
            percentage=80.0,
            passed=True,
            time_taken=250
        )
        
        self.result2 = QuizResult.objects.create(
            user=self.user,
            quiz=self.quiz2,
            score=60,
            total_possible=100,
            percentage=60.0,
            passed=False,
            time_taken=550
        )
        
        # 別ユーザーのクイズ結果
        self.result3 = QuizResult.objects.create(
            user=self.admin_user,
            quiz=self.quiz1,
            score=90,
            total_possible=100,
            percentage=90.0,
            passed=True,
            time_taken=200
        )
        
        # テスト用のURL
        self.list_url = reverse('quiz:quizresult-list')
    
    def test_list_quiz_results_as_normal_user(self):
        """通常ユーザーとしてのクイズ結果一覧取得テスト"""
        # クライアントに認証情報を設定
        self.client.force_authenticate(user=self.user)
        
        # APIリクエスト実行
        response = self.client.get(self.list_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 自分のクイズ結果のみ返されることを検証
        user_result_count = QuizResult.objects.filter(user=self.user).count()
        self.assertEqual(len(results), user_result_count)
        
        # 返された結果がすべて自分のものか検証
        for result in results:
            self.assertEqual(result['user'], self.user.pk)
    
    def test_list_quiz_results_as_admin(self):
        """管理者ユーザーとしてのクイズ結果一覧取得テスト"""
        # クライアントに認証情報を設定
        self.client.force_authenticate(user=self.admin_user)
        
        # APIリクエスト実行
        response = self.client.get(self.list_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # すべてのクイズ結果が返されることを検証
        all_result_count = QuizResult.objects.count()
        self.assertEqual(len(results), all_result_count)
    
    def test_retrieve_quiz_result(self):
        """個別のクイズ結果取得テスト"""
        # クライアントに認証情報を設定
        self.client.force_authenticate(user=self.user)
        
        # 詳細取得用URL
        detail_url = reverse('quiz:quizresult-detail', kwargs={'pk': self.result1.pk})
        
        # APIリクエスト実行
        response = self.client.get(detail_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 正しいクイズ結果が返されているか検証
        self.assertEqual(response.data['quiz'], self.quiz1.pk)
        self.assertEqual(response.data['score'], 80)
        self.assertEqual(response.data['passed'], True)
    
    def test_retrieve_other_user_result_as_normal_user(self):
        """通常ユーザーが他ユーザーのクイズ結果にアクセスするテスト"""
        # クライアントに認証情報を設定
        self.client.force_authenticate(user=self.user)
        
        # 他ユーザーの結果の詳細取得用URL
        detail_url = reverse('quiz:quizresult-detail', kwargs={'pk': self.result3.pk})
        
        # APIリクエスト実行
        response = self.client.get(detail_url)
        
        # アクセス拒否（404）となることを検証
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_retrieve_other_user_result_as_admin(self):
        """管理者ユーザーが他ユーザーのクイズ結果にアクセスするテスト"""
        # クライアントに認証情報を設定
        self.client.force_authenticate(user=self.admin_user)
        
        # 他ユーザーの結果の詳細取得用URL
        detail_url = reverse('quiz:quizresult-detail', kwargs={'pk': self.result1.pk})
        
        # APIリクエスト実行
        response = self.client.get(detail_url)
        
        # ステータスコードの検証（アクセス許可）
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 正しいクイズ結果が返されているか検証
        self.assertEqual(response.data['user'], self.user.pk)
        self.assertEqual(response.data['quiz'], self.quiz1.pk)
    
    def test_filter_quiz_results(self):
        """クイズ結果のフィルタリングテスト"""
        # クライアントに認証情報を設定
        self.client.force_authenticate(user=self.user)
        
        # クイズによるフィルタリング
        response = self.client.get(f"{self.list_url}?quiz={self.quiz1.pk}")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 指定したクイズの結果のみ返されることを検証
        quiz_count = QuizResult.objects.filter(user=self.user, quiz=self.quiz1).count()
        self.assertEqual(len(results), quiz_count)
        
        # passedによるフィルタリング
        response = self.client.get(f"{self.list_url}?passed=true")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # パスした結果のみ返されることを検証
        passed_count = QuizResult.objects.filter(user=self.user, passed=True).count()
        self.assertEqual(len(results), passed_count)
    
    def test_create_quiz_result(self):
        """クイズ結果作成テスト"""
        # クライアントに認証情報を設定
        self.client.force_authenticate(user=self.user)
        
        # 新しいクイズ結果のデータ
        data = {
            'user': self.user.pk,  # 明示的にユーザーIDを設定
            'quiz': self.quiz1.pk,
            'score': 75,
            'total_possible': 100,
            'percentage': 75.0,
            'time_taken': 280
        }
        
        # APIリクエスト実行
        response = self.client.post(self.list_url, data, format='json')
        
        # デバッグ用：レスポンスの詳細を出力
        print("\nレスポンスデータ:", response.data)
        print("ステータスコード:", response.status_code)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 作成されたクイズ結果の検証
        self.assertEqual(response.data['user'], self.user.pk)
        self.assertEqual(response.data['quiz'], self.quiz1.pk)
        self.assertEqual(response.data['score'], 75)
        self.assertEqual(response.data['passed'], True)  # 70点以上でパス
        
        # データベースに保存されたか検証
        self.assertTrue(
            QuizResult.objects.filter(
                user=self.user,
                quiz=self.quiz1,
                score=75
            ).exists()
        )
    
    def test_order_quiz_results(self):
        """クイズ結果の並び替えテスト"""
        # クライアントに認証情報を設定
        self.client.force_authenticate(user=self.user)
        
        # スコアの降順で並び替え
        response = self.client.get(f"{self.list_url}?ordering=-score")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # スコアの降順で正しくソートされているか検証
        if len(results) >= 2:
            self.assertGreaterEqual(results[0]['score'], results[1]['score'])


class UserStatisticsViewSetTests(APITestCase):
    """UserStatisticsViewSetに対するテスト"""
    
    def setUp(self):
        """テスト用データの初期化"""
        # テスト用カテゴリの作成
        self.category1 = Category.objects.create(
            name="Python",
            slug="python",
            description="Pythonプログラミングに関する問題",
            display_order=1,
            is_active=True
        )
        
        self.category2 = Category.objects.create(
            name="JavaScript",
            slug="javascript",
            description="JavaScriptプログラミングに関する問題",
            display_order=2,
            is_active=True
        )
        
        # テスト用の難易度レベルの作成
        self.level1 = DifficultyLevel.objects.create(
            name="初級",
            slug="beginner",
            level=1,
            description="プログラミング初心者向けの基本的な問題",
            point_multiplier=1.0,
            time_limit=300
        )
        
        self.level2 = DifficultyLevel.objects.create(
            name="中級",
            slug="intermediate",
            level=2,
            description="基本を理解している人向けの応用問題",
            point_multiplier=1.5,
            time_limit=600
        )
        
        # テスト用ユーザーの作成
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # テスト用管理者ユーザーの作成
        self.admin_user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword',
            is_staff=True
        )
        
        # ユーザー統計情報の作成（カテゴリ1に対する統計）
        self.stats1 = UserStatistics.objects.create(
            user=self.user,
            category=self.category1,
            difficulty=None,
            quizzes_completed=5,
            total_points=450,
            avg_score=90.0,
            highest_score=100.0
        )
        
        # ユーザー統計情報の作成（カテゴリ2に対する統計）
        self.stats2 = UserStatistics.objects.create(
            user=self.user,
            category=self.category2,
            difficulty=None,
            quizzes_completed=3,
            total_points=240,
            avg_score=80.0,
            highest_score=90.0
        )
        
        # 難易度別の統計情報
        self.stats3 = UserStatistics.objects.create(
            user=self.user,
            category=None,
            difficulty=self.level1,
            quizzes_completed=4,
            total_points=350,
            avg_score=87.5,
            highest_score=100.0
        )
        
        # 別ユーザーの統計情報
        self.stats4 = UserStatistics.objects.create(
            user=self.admin_user,
            category=self.category1,
            difficulty=None,
            quizzes_completed=2,
            total_points=180,
            avg_score=90.0,
            highest_score=95.0
        )
        
        # テスト用のURL
        self.list_url = reverse('quiz:userstatistics-list')
        self.summary_url = reverse('quiz:userstatistics-summary')
    
    def test_list_statistics_as_normal_user(self):
        """通常ユーザーとしての統計情報一覧取得テスト"""
        # クライアントに認証情報を設定
        self.client.force_authenticate(user=self.user)
        
        # APIリクエスト実行
        response = self.client.get(self.list_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 自分の統計情報のみ返されることを検証
        from quiz.models import UserStatistics
        user_stats_count = UserStatistics.objects.filter(user=self.user).count()
        self.assertEqual(len(results), user_stats_count)
        
        # 返された統計情報がすべて自分のものか検証
        for stat in results:
            self.assertEqual(stat['user'], self.user.pk)
    
    def test_list_statistics_as_admin(self):
        """管理者ユーザーとしての統計情報一覧取得テスト"""
        # クライアントに認証情報を設定
        self.client.force_authenticate(user=self.admin_user)
        
        # APIリクエスト実行
        response = self.client.get(self.list_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # すべての統計情報が返されることを検証
        from quiz.models import UserStatistics
        all_stats_count = UserStatistics.objects.count()
        self.assertEqual(len(results), all_stats_count)
    
    def test_retrieve_statistics(self):
        """個別の統計情報取得テスト"""
        # クライアントに認証情報を設定
        self.client.force_authenticate(user=self.user)
        
        # 詳細取得用URL
        detail_url = reverse('quiz:userstatistics-detail', kwargs={'pk': self.stats1.pk})
        
        # APIリクエスト実行
        response = self.client.get(detail_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 正しい統計情報が返されているか検証
        self.assertEqual(response.data['user'], self.user.pk)
        self.assertEqual(response.data['category'], self.category1.pk)
        self.assertEqual(response.data['quizzes_completed'], 5)
        self.assertEqual(response.data['total_points'], 450)
        self.assertEqual(response.data['avg_score'], 90.0)
    
    def test_retrieve_other_user_statistics_as_normal_user(self):
        """通常ユーザーが他ユーザーの統計情報にアクセスするテスト"""
        # クライアントに認証情報を設定
        self.client.force_authenticate(user=self.user)
        
        # 他ユーザーの統計情報の詳細取得用URL
        detail_url = reverse('quiz:userstatistics-detail', kwargs={'pk': self.stats4.pk})
        
        # APIリクエスト実行
        response = self.client.get(detail_url)
        
        # アクセス拒否（404）となることを検証
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_filter_statistics(self):
        """統計情報のフィルタリングテスト"""
        # クライアントに認証情報を設定
        self.client.force_authenticate(user=self.user)
        
        # カテゴリによるフィルタリング
        response = self.client.get(f"{self.list_url}?category={self.category1.pk}")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 指定したカテゴリの統計情報のみ返されることを検証
        from quiz.models import UserStatistics
        category_stats_count = UserStatistics.objects.filter(
            user=self.user, 
            category=self.category1
        ).count()
        self.assertEqual(len(results), category_stats_count)
        
        # 難易度によるフィルタリング
        response = self.client.get(f"{self.list_url}?difficulty={self.level1.pk}")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 指定した難易度の統計情報のみ返されることを検証
        difficulty_stats_count = UserStatistics.objects.filter(
            user=self.user, 
            difficulty=self.level1
        ).count()
        self.assertEqual(len(results), difficulty_stats_count)
    
    def test_order_statistics(self):
        """統計情報の並び替えテスト"""
        # クライアントに認証情報を設定
        self.client.force_authenticate(user=self.user)
        
        # クイズ完了数の降順で並び替え
        response = self.client.get(f"{self.list_url}?ordering=-quizzes_completed")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # クイズ完了数の降順で正しくソートされているか検証
        if len(results) >= 2:
            self.assertGreaterEqual(results[0]['quizzes_completed'], results[1]['quizzes_completed'])
    
    def test_summary_endpoint(self):
        """統計情報サマリーエンドポイントのテスト"""
        # クライアントに認証情報を設定
        self.client.force_authenticate(user=self.user)
        
        # APIリクエスト実行
        response = self.client.get(self.summary_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # サマリー情報の検証
        self.assertIn('total_quizzes_completed', response.data)
        self.assertIn('total_points', response.data)
        self.assertIn('overall_avg_score', response.data)
        self.assertIn('categories', response.data)
        self.assertIn('difficulties', response.data)
        
        # 合計値の検証
        from quiz.models import UserStatistics
        user_stats = UserStatistics.objects.filter(user=self.user)
        expected_total_quizzes = sum(stat.quizzes_completed for stat in user_stats)
        self.assertEqual(response.data['total_quizzes_completed'], expected_total_quizzes)
        
        # カテゴリ情報の検証
        self.assertEqual(len(response.data['categories']), 2)  # 2つのカテゴリの統計情報
        
        # 難易度情報の検証
        self.assertEqual(len(response.data['difficulties']), 1)  # 1つの難易度の統計情報


class ActivityHistoryViewSetTests(APITestCase):
    """ActivityHistoryViewSetに対するテスト"""
    
    def setUp(self):
        """テスト用データの初期化"""
        # テスト用カテゴリの作成
        self.category = Category.objects.create(
            name="Python",
            slug="python",
            description="Pythonプログラミングに関する問題",
            display_order=1,
            is_active=True
        )
        
        # テスト用の難易度レベルの作成
        self.level = DifficultyLevel.objects.create(
            name="初級",
            slug="beginner",
            level=1,
            description="プログラミング初心者向けの基本的な問題",
            point_multiplier=1.0,
            time_limit=300
        )
        
        # テスト用クイズの作成
        self.quiz = Quiz.objects.create(
            category=self.category,
            difficulty=self.level,
            title="Python基礎クイズ",
            description="Pythonの基本構文や概念に関するクイズ",
            time_limit=300,
            pass_score=70,
            is_active=True
        )
        
        # テスト用ユーザーの作成
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        # テスト用管理者ユーザーの作成
        self.admin_user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='adminpassword',
            is_staff=True
        )
        
        # 活動履歴の作成
        from quiz.models import ActivityHistory
        from datetime import datetime, timedelta
        
        # 今日の活動
        self.activity1 = ActivityHistory.objects.create(
            user=self.user,
            quiz=self.quiz,
            category=self.category,
            difficulty=self.level,
            activity_type='quiz_completed',
            score=85,
            percentage=85.0,
            activity_date=datetime.now()
        )
        
        # 昨日の活動
        self.activity2 = ActivityHistory.objects.create(
            user=self.user,
            quiz=self.quiz,
            category=self.category,
            difficulty=self.level,
            activity_type='quiz_completed',
            score=75,
            percentage=75.0,
            activity_date=datetime.now() - timedelta(days=1)
        )
        
        # 一週間前の活動
        self.activity3 = ActivityHistory.objects.create(
            user=self.user,
            quiz=self.quiz,
            category=self.category,
            difficulty=self.level,
            activity_type='quiz_started',
            score=0,
            percentage=0,
            activity_date=datetime.now() - timedelta(days=7)
        )
        
        # 別ユーザーの活動
        self.activity4 = ActivityHistory.objects.create(
            user=self.admin_user,
            quiz=self.quiz,
            category=self.category,
            difficulty=self.level,
            activity_type='quiz_completed',
            score=90,
            percentage=90.0,
            activity_date=datetime.now()
        )
        
        # テスト用のURL
        self.list_url = reverse('quiz:activityhistory-list')
        self.recent_url = reverse('quiz:activityhistory-recent')
    
    def test_list_activities_as_normal_user(self):
        """通常ユーザーとしての活動履歴一覧取得テスト"""
        # クライアントに認証情報を設定
        self.client.force_authenticate(user=self.user)
        
        # APIリクエスト実行
        response = self.client.get(self.list_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 自分の活動履歴のみ返されることを検証
        from quiz.models import ActivityHistory
        user_activity_count = ActivityHistory.objects.filter(user=self.user).count()
        self.assertEqual(len(results), user_activity_count)
        
        # 返された活動履歴がすべて自分のものか検証
        for activity in results:
            self.assertEqual(activity['user'], self.user.pk)
    
    def test_list_activities_as_admin(self):
        """管理者ユーザーとしての活動履歴一覧取得テスト"""
        # クライアントに認証情報を設定
        self.client.force_authenticate(user=self.admin_user)
        
        # APIリクエスト実行
        response = self.client.get(self.list_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # すべての活動履歴が返されることを検証
        from quiz.models import ActivityHistory
        all_activity_count = ActivityHistory.objects.count()
        self.assertEqual(len(results), all_activity_count)
    
    def test_retrieve_activity(self):
        """個別の活動履歴取得テスト"""
        # クライアントに認証情報を設定
        self.client.force_authenticate(user=self.user)
        
        # 詳細取得用URL
        detail_url = reverse('quiz:activityhistory-detail', kwargs={'pk': self.activity1.pk})
        
        # APIリクエスト実行
        response = self.client.get(detail_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 正しい活動履歴が返されているか検証
        self.assertEqual(response.data['user'], self.user.pk)
        self.assertEqual(response.data['quiz'], self.quiz.pk)
        self.assertEqual(response.data['activity_type'], 'quiz_completed')
        self.assertEqual(response.data['score'], 85)
    
    def test_retrieve_other_user_activity_as_normal_user(self):
        """通常ユーザーが他ユーザーの活動履歴にアクセスするテスト"""
        # クライアントに認証情報を設定
        self.client.force_authenticate(user=self.user)
        
        # 他ユーザーの活動履歴の詳細取得用URL
        detail_url = reverse('quiz:activityhistory-detail', kwargs={'pk': self.activity4.pk})
        
        # APIリクエスト実行
        response = self.client.get(detail_url)
        
        # アクセス拒否（404）となることを検証
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_filter_activities(self):
        """活動履歴のフィルタリングテスト"""
        # クライアントに認証情報を設定
        self.client.force_authenticate(user=self.user)
        
        # 活動タイプによるフィルタリング
        response = self.client.get(f"{self.list_url}?activity_type=quiz_completed")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 指定した活動タイプの履歴のみ返されることを検証
        from quiz.models import ActivityHistory
        completed_count = ActivityHistory.objects.filter(
            user=self.user, 
            activity_type='quiz_completed'
        ).count()
        self.assertEqual(len(results), completed_count)
        
        # 返された活動履歴がすべて指定したタイプか検証
        for activity in results:
            self.assertEqual(activity['activity_type'], 'quiz_completed')
    
    def test_order_activities(self):
        """活動履歴の並び替えテスト"""
        # クライアントに認証情報を設定
        self.client.force_authenticate(user=self.user)
        
        # 活動日時の降順で並び替え（デフォルト）
        response = self.client.get(self.list_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # レスポンスデータの検証 (ペジネーション形式に対応)
        self.assertIn('results', response.data)
        results = response.data['results']
        
        # 活動日時の降順で正しくソートされているか検証
        if len(results) >= 2:
            date1 = datetime.fromisoformat(results[0]['activity_date'].replace('Z', '+00:00'))
            date2 = datetime.fromisoformat(results[1]['activity_date'].replace('Z', '+00:00'))
            self.assertGreaterEqual(date1, date2)
    
    def test_recent_endpoint(self):
        """最近の活動履歴エンドポイントのテスト"""
        # クライアントに認証情報を設定
        self.client.force_authenticate(user=self.user)
        
        # APIリクエスト実行（デフォルトで10件）
        response = self.client.get(self.recent_url)
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # データの検証
        self.assertEqual(len(response.data), 3)  # 3件の活動履歴がある
        
        # 制限付きの取得テスト
        response = self.client.get(f"{self.recent_url}?limit=2")
        
        # ステータスコードの検証
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # データの検証
        self.assertEqual(len(response.data), 2)  # 制限が2件
        
        # 最新の活動が最初に来ているか検証（日付順）
        if len(response.data) >= 2:
            date1 = datetime.fromisoformat(response.data[0]['activity_date'].replace('Z', '+00:00'))
            date2 = datetime.fromisoformat(response.data[1]['activity_date'].replace('Z', '+00:00'))
            self.assertGreaterEqual(date1, date2)  # 最新のものが先に来ていることを検証