"""
Quizアプリケーションのモデル単体テスト
"""

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from datetime import datetime, timedelta

from quiz.models import (
    Category, DifficultyLevel, Quiz, Question, Answer, 
    QuizResult, UserStatistics, ActivityHistory
)


class CategoryModelTest(TestCase):
    """Categoryモデルのテストケース"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.category_data = {
            'name': 'HTML & CSS',
            'description': 'HTML and CSS fundamentals',
            'icon': 'html5',
            'display_order': 1,
            'is_active': True
        }
    
    def test_category_creation(self):
        """カテゴリの正常な作成をテスト"""
        category = Category.objects.create(**self.category_data)
        
        self.assertEqual(category.name, 'HTML & CSS')
        self.assertEqual(category.description, 'HTML and CSS fundamentals')
        self.assertEqual(category.icon, 'html5')
        self.assertEqual(category.display_order, 1)
        self.assertTrue(category.is_active)
        self.assertIsNotNone(category.created_at)
        self.assertIsNotNone(category.updated_at)
    
    def test_category_str_method(self):
        """__str__メソッドのテスト"""
        category = Category.objects.create(**self.category_data)
        self.assertEqual(str(category), 'HTML & CSS')
    
    def test_slug_auto_generation(self):
        """スラッグの自動生成をテスト"""
        category = Category.objects.create(**self.category_data)
        expected_slug = slugify('HTML & CSS')
        self.assertEqual(category.slug, expected_slug)
    
    def test_slug_uniqueness(self):
        """スラッグの一意性をテスト（同じ名前の場合）"""
        # 最初のカテゴリを作成
        category1 = Category.objects.create(**self.category_data)
        
        # 同じ名前で2つ目のカテゴリを作成
        category2 = Category.objects.create(**self.category_data)
        
        # 2つ目のスラッグは数字が追加されるはず
        self.assertNotEqual(category1.slug, category2.slug)
        self.assertTrue(category2.slug.endswith('-1'))
    
    def test_category_ordering(self):
        """カテゴリの並び順をテスト"""
        category1 = Category.objects.create(name='Second', display_order=2)
        category2 = Category.objects.create(name='First', display_order=1)
        
        categories = list(Category.objects.all())
        self.assertEqual(categories[0], category2)  # display_order=1が先
        self.assertEqual(categories[1], category1)  # display_order=2が後


class DifficultyLevelModelTest(TestCase):
    """DifficultyLevelモデルのテストケース"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.difficulty_data = {
            'name': '初級',
            'level': 1,
            'description': '基本的な問題',
            'point_multiplier': 1,
            'time_limit': 300
        }
    
    def test_difficulty_creation(self):
        """難易度の正常な作成をテスト"""
        difficulty = DifficultyLevel.objects.create(**self.difficulty_data)
        
        self.assertEqual(difficulty.name, '初級')
        self.assertEqual(difficulty.level, 1)
        self.assertEqual(difficulty.description, '基本的な問題')
        self.assertEqual(difficulty.point_multiplier, 1)
        self.assertEqual(difficulty.time_limit, 300)
    
    def test_difficulty_str_method(self):
        """__str__メソッドのテスト"""
        difficulty = DifficultyLevel.objects.create(**self.difficulty_data)
        self.assertEqual(str(difficulty), '初級')
    
    def test_level_uniqueness(self):
        """レベル値の一意性をテスト"""
        DifficultyLevel.objects.create(**self.difficulty_data)
        
        # 同じレベル値で作成を試みる
        with self.assertRaises(IntegrityError):
            DifficultyLevel.objects.create(
                name='別の初級',
                level=1  # 同じレベル値
            )
    
    def test_difficulty_ordering(self):
        """難易度の並び順をテスト"""
        difficulty3 = DifficultyLevel.objects.create(name='上級', level=3)
        difficulty1 = DifficultyLevel.objects.create(name='初級', level=1)
        difficulty2 = DifficultyLevel.objects.create(name='中級', level=2)
        
        difficulties = list(DifficultyLevel.objects.all())
        self.assertEqual(difficulties[0], difficulty1)  # level=1が先
        self.assertEqual(difficulties[1], difficulty2)  # level=2が次
        self.assertEqual(difficulties[2], difficulty3)  # level=3が最後


class QuizModelTest(TestCase):
    """Quizモデルのテストケース"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.category = Category.objects.create(
            name='HTML & CSS',
            display_order=1
        )
        self.difficulty = DifficultyLevel.objects.create(
            name='初級',
            level=1
        )
        self.quiz_data = {
            'category': self.category,
            'difficulty': self.difficulty,
            'title': 'HTML基礎クイズ',
            'description': 'HTMLの基本的な内容のクイズです',
            'time_limit': 600,
            'pass_score': 70,
            'is_active': True
        }
    
    def test_quiz_creation(self):
        """クイズの正常な作成をテスト"""
        quiz = Quiz.objects.create(**self.quiz_data)
        
        self.assertEqual(quiz.category, self.category)
        self.assertEqual(quiz.difficulty, self.difficulty)
        self.assertEqual(quiz.title, 'HTML基礎クイズ')
        self.assertEqual(quiz.description, 'HTMLの基本的な内容のクイズです')
        self.assertEqual(quiz.time_limit, 600)
        self.assertEqual(quiz.pass_score, 70)
        self.assertTrue(quiz.is_active)
    
    def test_quiz_str_method(self):
        """__str__メソッドのテスト"""
        quiz = Quiz.objects.create(**self.quiz_data)
        expected_str = f"{quiz.title} ({self.category.name} - {self.difficulty.name})"
        self.assertEqual(str(quiz), expected_str)
    
    def test_quiz_foreign_key_relationships(self):
        """外部キーの関連性をテスト"""
        quiz = Quiz.objects.create(**self.quiz_data)
        
        # カテゴリから逆参照
        self.assertIn(quiz, self.category.quizzes.all())
        
        # 難易度から逆参照
        self.assertIn(quiz, self.difficulty.quizzes.all())
    
    def test_quiz_cascade_deletion(self):
        """カスケード削除をテスト"""
        quiz = Quiz.objects.create(**self.quiz_data)
        quiz_id = quiz.id
        
        # カテゴリを削除すると、関連するクイズも削除される
        self.category.delete()
        
        with self.assertRaises(Quiz.DoesNotExist):
            Quiz.objects.get(id=quiz_id)


class QuestionModelTest(TestCase):
    """Questionモデルのテストケース"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.category = Category.objects.create(name='HTML & CSS')
        self.difficulty = DifficultyLevel.objects.create(name='初級', level=1)
        self.quiz = Quiz.objects.create(
            category=self.category,
            difficulty=self.difficulty,
            title='テストクイズ'
        )
        self.question_data = {
            'quiz': self.quiz,
            'question_text': 'HTMLの正式名称は何ですか？',
            'explanation': 'HyperText Markup Languageの略です',
            'hint': 'マークアップ言語です',
            'display_order': 1,
            'points': 10
        }
    
    def test_question_creation(self):
        """問題の正常な作成をテスト"""
        question = Question.objects.create(**self.question_data)
        
        self.assertEqual(question.quiz, self.quiz)
        self.assertEqual(question.question_text, 'HTMLの正式名称は何ですか？')
        self.assertEqual(question.explanation, 'HyperText Markup Languageの略です')
        self.assertEqual(question.hint, 'マークアップ言語です')
        self.assertEqual(question.display_order, 1)
        self.assertEqual(question.points, 10)
    
    def test_question_str_method(self):
        """__str__メソッドのテスト"""
        question = Question.objects.create(**self.question_data)
        expected_str = f"{question.quiz.title} - 問題{question.display_order}: {question.question_text[:30]}..."
        self.assertEqual(str(question), expected_str)
    
    def test_question_ordering(self):
        """問題の並び順をテスト"""
        question2 = Question.objects.create(
            quiz=self.quiz,
            question_text='問題2',
            display_order=2
        )
        question1 = Question.objects.create(
            quiz=self.quiz,
            question_text='問題1',
            display_order=1
        )
        
        questions = list(Question.objects.all())
        self.assertEqual(questions[0], question1)  # display_order=1が先
        self.assertEqual(questions[1], question2)  # display_order=2が後


class AnswerModelTest(TestCase):
    """Answerモデルのテストケース"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.category = Category.objects.create(name='HTML & CSS')
        self.difficulty = DifficultyLevel.objects.create(name='初級', level=1)
        self.quiz = Quiz.objects.create(
            category=self.category,
            difficulty=self.difficulty,
            title='テストクイズ'
        )
        self.question = Question.objects.create(
            quiz=self.quiz,
            question_text='HTMLの正式名称は何ですか？',
            display_order=1
        )
        self.answer_data = {
            'question': self.question,
            'answer_text': 'HyperText Markup Language',
            'is_correct': True,
            'display_order': 1
        }
    
    def test_answer_creation(self):
        """回答選択肢の正常な作成をテスト"""
        answer = Answer.objects.create(**self.answer_data)
        
        self.assertEqual(answer.question, self.question)
        self.assertEqual(answer.answer_text, 'HyperText Markup Language')
        self.assertTrue(answer.is_correct)
        self.assertEqual(answer.display_order, 1)
    
    def test_answer_str_method(self):
        """__str__メソッドのテスト"""
        answer = Answer.objects.create(**self.answer_data)
        expected_str = f"{answer.question.quiz.title} - 問題{answer.question.display_order} - 回答: {answer.answer_text[:20]}... [{'✓' if answer.is_correct else '✗'}]"
        self.assertEqual(str(answer), expected_str)
    
    def test_multiple_answers_per_question(self):
        """1つの問題に複数の回答選択肢をテスト"""
        correct_answer = Answer.objects.create(**self.answer_data)
        incorrect_answer = Answer.objects.create(
            question=self.question,
            answer_text='間違った答え',
            is_correct=False,
            display_order=2
        )
        
        answers = list(self.question.answers.all())
        self.assertEqual(len(answers), 2)
        self.assertIn(correct_answer, answers)
        self.assertIn(incorrect_answer, answers)


class QuizResultModelTest(TestCase):
    """QuizResultモデルのテストケース"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='HTML & CSS')
        self.difficulty = DifficultyLevel.objects.create(name='初級', level=1)
        self.quiz = Quiz.objects.create(
            category=self.category,
            difficulty=self.difficulty,
            title='テストクイズ'
        )
        self.result_data = {
            'user': self.user,
            'quiz': self.quiz,
            'score': 85,
            'total_possible': 100,
            'percentage': 85.0,
            'time_taken': 300,
            'passed': True
        }
    
    def test_quiz_result_creation(self):
        """クイズ結果の正常な作成をテスト"""
        result = QuizResult.objects.create(**self.result_data)
        
        self.assertEqual(result.user, self.user)
        self.assertEqual(result.quiz, self.quiz)
        self.assertEqual(result.score, 85)
        self.assertEqual(result.total_possible, 100)
        self.assertEqual(result.percentage, 85.0)
        self.assertEqual(result.time_taken, 300)
        self.assertTrue(result.passed)
    
    def test_quiz_result_str_method(self):
        """__str__メソッドのテスト"""
        result = QuizResult.objects.create(**self.result_data)
        expected_str = f"{self.user.username} - {self.quiz.title} - {result.score}/{result.total_possible}点 ({result.percentage:.1f}%) [{'合格' if result.passed else '不合格'}]"
        self.assertEqual(str(result), expected_str)
    
    def test_quiz_result_relationships(self):
        """関連性をテスト"""
        result = QuizResult.objects.create(**self.result_data)
        
        # ユーザーから逆参照
        self.assertIn(result, self.user.quiz_results.all())
        
        # クイズから逆参照
        self.assertIn(result, self.quiz.results.all())


class UserStatisticsModelTest(TestCase):
    """UserStatisticsモデルのテストケース"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.stats_data = {
            'user': self.user,
            'quizzes_completed': 5,
            'total_points': 400,
            'avg_score': 80.0,
            'highest_score': 95
        }
    
    def test_user_statistics_creation(self):
        """ユーザー統計の正常な作成をテスト"""
        stats = UserStatistics.objects.create(**self.stats_data)
        
        self.assertEqual(stats.user, self.user)
        self.assertEqual(stats.quizzes_completed, 5)
        self.assertEqual(stats.total_points, 400)
        self.assertEqual(stats.avg_score, 80.0)
        self.assertEqual(stats.highest_score, 95)
    
    def test_user_statistics_str_method(self):
        """__str__メソッドのテスト"""
        stats = UserStatistics.objects.create(**self.stats_data)
        expected_str = f"{self.user.username} - 全カテゴリ - 全難易度 - 完了: {stats.quizzes_completed}回, 平均: {stats.avg_score:.1f}%"
        self.assertEqual(str(stats), expected_str)
    
    def test_user_statistics_multiple_entries(self):
        """ユーザーの複数統計情報をテスト"""
        # カテゴリ・難易度別の統計情報
        category = Category.objects.create(name='JavaScript')
        difficulty = DifficultyLevel.objects.create(name='中級', level=2)
        
        stats1 = UserStatistics.objects.create(**self.stats_data)
        stats2 = UserStatistics.objects.create(
            user=self.user,
            category=category,
            difficulty=difficulty,
            quizzes_completed=3,
            total_points=180,
            avg_score=60.0
        )
        
        # ユーザーから統計情報への逆参照
        user_stats = self.user.statistics.all()
        self.assertEqual(len(user_stats), 2)
        self.assertIn(stats1, user_stats)
        self.assertIn(stats2, user_stats)


class ActivityHistoryModelTest(TestCase):
    """ActivityHistoryモデルのテストケース"""
    
    def setUp(self):
        """テスト用データの準備"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(name='HTML & CSS')
        self.difficulty = DifficultyLevel.objects.create(name='初級', level=1)
        self.quiz = Quiz.objects.create(
            category=self.category,
            difficulty=self.difficulty,
            title='テストクイズ'
        )
        self.quiz_result = QuizResult.objects.create(
            user=self.user,
            quiz=self.quiz,
            score=85,
            total_possible=100,
            percentage=85.0,
            time_taken=300
        )
        self.activity_data = {
            'user': self.user,
            'quiz': self.quiz,
            'category': self.category,
            'difficulty': self.difficulty,
            'score': 85,
            'percentage': 85.0,
            'activity_date': timezone.now()
        }
    
    def test_activity_history_creation(self):
        """活動履歴の正常な作成をテスト"""
        activity = ActivityHistory.objects.create(**self.activity_data)
        
        self.assertEqual(activity.user, self.user)
        self.assertEqual(activity.quiz, self.quiz)
        self.assertEqual(activity.category, self.category)
        self.assertEqual(activity.difficulty, self.difficulty)
        self.assertEqual(activity.score, 85)
        self.assertEqual(activity.percentage, 85.0)
        self.assertIsNotNone(activity.activity_date)
    
    def test_activity_history_str_method(self):
        """__str__メソッドのテスト"""
        activity = ActivityHistory.objects.create(**self.activity_data)
        expected_str = f"{self.user.username} - クイズ完了 - {self.quiz.title} - {activity.score}点 ({activity.percentage:.1f}%)"
        self.assertEqual(str(activity), expected_str)
    
    def test_activity_history_ordering(self):
        """活動履歴の並び順をテスト（新しい順）"""
        # 古い活動
        old_activity = ActivityHistory.objects.create(
            user=self.user,
            quiz=self.quiz,
            category=self.category,
            difficulty=self.difficulty,
            score=70,
            percentage=70.0,
            activity_date=timezone.now() - timedelta(days=1)
        )
        
        # 新しい活動
        new_activity = ActivityHistory.objects.create(**self.activity_data)
        
        activities = list(ActivityHistory.objects.all())
        self.assertEqual(activities[0], new_activity)  # 新しいものが先
        self.assertEqual(activities[1], old_activity)  # 古いものが後
    
    def test_recent_activities_queryset(self):
        """最近の活動取得のクエリセットをテスト"""
        # 複数の活動履歴を作成
        for i in range(5):
            ActivityHistory.objects.create(
                user=self.user,
                quiz=self.quiz,
                category=self.category,
                difficulty=self.difficulty,
                score=80 + i,
                percentage=80.0 + i,
                activity_date=timezone.now() - timedelta(hours=i)
            )
        
        # 最新3件を取得
        recent_activities = ActivityHistory.objects.all()[:3]
        self.assertEqual(len(recent_activities), 3)
        
        # スコアが降順になっているかチェック（最新が高いスコア）
        scores = [activity.score for activity in recent_activities]
        self.assertEqual(scores, [84, 83, 82])


class ModelIntegrationTest(TestCase):
    """モデル間の統合テスト"""
    
    def setUp(self):
        """複数モデルを使った統合テスト用データの準備"""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.category = Category.objects.create(
            name='HTML & CSS',
            display_order=1
        )
        self.difficulty = DifficultyLevel.objects.create(
            name='初級',
            level=1
        )
        self.quiz = Quiz.objects.create(
            category=self.category,
            difficulty=self.difficulty,
            title='HTML基礎クイズ'
        )
        
        # 問題と回答選択肢を作成
        self.question = Question.objects.create(
            quiz=self.quiz,
            question_text='HTMLの正式名称は何ですか？',
            display_order=1,
            points=10
        )
        self.correct_answer = Answer.objects.create(
            question=self.question,
            answer_text='HyperText Markup Language',
            is_correct=True,
            display_order=1
        )
        self.incorrect_answer = Answer.objects.create(
            question=self.question,
            answer_text='間違った答え',
            is_correct=False,
            display_order=2
        )
    
    def test_full_quiz_workflow(self):
        """完全なクイズワークフローのテスト"""
        # クイズ結果を作成
        quiz_result = QuizResult.objects.create(
            user=self.user,
            quiz=self.quiz,
            score=90,
            total_possible=100,
            percentage=90.0,
            time_taken=120,
            passed=True
        )
        
        # 活動履歴を作成
        activity = ActivityHistory.objects.create(
            user=self.user,
            quiz=self.quiz,
            category=self.category,
            difficulty=self.difficulty,
            score=90,
            percentage=90.0
        )
        
        # ユーザー統計を作成
        stats = UserStatistics.objects.create(
            user=self.user,
            quizzes_completed=1,
            total_points=90,
            avg_score=90.0
        )
        
        # 全ての関連付けが正しく動作することを確認
        self.assertEqual(quiz_result.user, self.user)
        self.assertEqual(quiz_result.quiz, self.quiz)
        self.assertEqual(activity.quiz, self.quiz)
        self.assertEqual(activity.category, self.category)
        self.assertEqual(stats.user, self.user)
        
        # 逆参照の確認
        self.assertIn(quiz_result, self.user.quiz_results.all())
        self.assertIn(activity, self.user.activity_history.all())
        self.assertIn(stats, self.user.statistics.all())
    
    def test_cascade_deletions(self):
        """カスケード削除のテスト"""
        quiz_result = QuizResult.objects.create(
            user=self.user,
            quiz=self.quiz,
            score=80,
            total_possible=100,
            percentage=80.0,
            time_taken=240
        )
        
        quiz_id = self.quiz.id
        question_id = self.question.id
        answer_ids = [self.correct_answer.id, self.incorrect_answer.id]
        
        # カテゴリを削除
        self.category.delete()
        
        # 関連するオブジェクトが全て削除されることを確認
        with self.assertRaises(Quiz.DoesNotExist):
            Quiz.objects.get(id=quiz_id)
        
        with self.assertRaises(Question.DoesNotExist):
            Question.objects.get(id=question_id)
        
        for answer_id in answer_ids:
            with self.assertRaises(Answer.DoesNotExist):
                Answer.objects.get(id=answer_id)
        
        # QuizResultも削除される
        with self.assertRaises(QuizResult.DoesNotExist):
            QuizResult.objects.get(id=quiz_result.id)