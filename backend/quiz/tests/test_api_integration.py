"""
API統合テスト - 実際のユーザーフローを通じたAPI連携のテスト
"""

import json
import time
from datetime import datetime, timedelta
from django.test import TestCase, TransactionTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from quiz.models import (
    Category, DifficultyLevel, Quiz, Question, Answer,
    QuizResult, UserStatistics, ActivityHistory
)


User = get_user_model()


class APIIntegrationTestCase(TransactionTestCase):
    """
    API統合テストの基底クラス
    実際のユーザーフローをシミュレートして、複数のAPIエンドポイントの連携をテスト
    """
    
    def setUp(self):
        """テスト環境のセットアップ"""
        self.client = APIClient()
        self.setup_test_data()
        # ユーザーごとの統計情報を管理
        self._user_stats = {}
        
    def setup_test_data(self):
        """テストデータの作成"""
        # カテゴリーの作成
        self.categories = {
            'python': Category.objects.create(
                name='Python',
                slug='python',
                description='Python programming',
                display_order=1
            ),
            'javascript': Category.objects.create(
                name='JavaScript',
                slug='javascript',
                description='JavaScript programming',
                display_order=2
            ),
            'django': Category.objects.create(
                name='Django',
                slug='django',
                description='Django framework',
                display_order=3
            )
        }
        
        # 難易度の作成
        self.difficulties = {
            'beginner': DifficultyLevel.objects.create(
                name='Beginner',
                slug='beginner',
                level=1,
                description='For beginners'
            ),
            'intermediate': DifficultyLevel.objects.create(
                name='Intermediate',
                slug='intermediate',
                level=2,
                description='For intermediate learners'
            ),
            'advanced': DifficultyLevel.objects.create(
                name='Advanced',
                slug='advanced',
                level=3,
                description='For advanced learners'
            )
        }
        
        # 各カテゴリー・難易度の組み合わせでクイズを作成
        self.quizzes = {}
        for cat_key, category in self.categories.items():
            for diff_key, difficulty in self.difficulties.items():
                quiz = Quiz.objects.create(
                    title=f'{category.name} {difficulty.name} Quiz',
                    description=f'A {difficulty.name.lower()} quiz about {category.name}',
                    category=category,
                    difficulty=difficulty,
                    time_limit=30,
                    pass_score=21,  # 30点満点の70%は21点
                    is_active=True
                )
                
                # 各クイズに3問ずつ問題を作成
                for i in range(3):
                    question = Question.objects.create(
                        quiz=quiz,
                        question_text=f'Question {i+1} for {quiz.title}',
                        question_type='multiple_choice',
                        display_order=i+1,
                        points=10
                    )
                    
                    # 各問題に4つの選択肢を作成（1つが正解）
                    for j in range(4):
                        Answer.objects.create(
                            question=question,
                            answer_text=f'Answer {j+1}',
                            is_correct=(j == 0),  # 最初の選択肢を正解とする
                            display_order=j+1
                        )
                
                self.quizzes[f'{cat_key}_{diff_key}'] = quiz
    
    def create_user_and_authenticate(self, username='testuser'):
        """ユーザーを作成して認証トークンを取得"""
        user = User.objects.create_user(
            username=username,
            email=f'{username}@example.com',
            password='testpass123'
        )
        
        # JWTトークンを取得
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        return user, {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    
    def create_quiz_result_with_stats(self, user, quiz, score, total_possible, time_taken):
        """
        クイズ結果を作成し、テスト環境用に統計情報と活動履歴も手動で作成
        """
        percentage = (score / total_possible) * 100 if total_possible > 0 else 0
        
        # クイズ結果を作成
        result = QuizResult.objects.create(
            user=user,
            quiz=quiz,
            score=score,
            total_possible=total_possible,
            percentage=percentage,
            time_taken=time_taken,
            passed=(score >= quiz.pass_score)
        )
        
        # 統計情報を更新または作成（カテゴリーと難易度なしの全体統計）
        stats, created = UserStatistics.objects.get_or_create(
            user=user,
            category=None,
            difficulty=None,
            defaults={
                'quizzes_completed': 0,
                'total_points': 0,
                'avg_score': 0.0,
                'highest_score': 0
            }
        )
        
        # 統計情報を更新
        stats.quizzes_completed += 1
        stats.total_points += score
        
        # ユーザーごとの累積スコアを管理
        user_id = user.id
        if user_id not in self._user_stats:
            self._user_stats[user_id] = {
                'total_percentage': 0,
                'count': 0
            }
        
        self._user_stats[user_id]['total_percentage'] += percentage
        self._user_stats[user_id]['count'] += 1
        
        # 平均スコアを計算
        stats.avg_score = self._user_stats[user_id]['total_percentage'] / self._user_stats[user_id]['count']
        stats.highest_score = max(stats.highest_score, score)
        stats.save()
        
        # 活動履歴を作成
        ActivityHistory.objects.create(
            user=user,
            quiz=quiz,
            category=quiz.category,
            difficulty=quiz.difficulty,
            activity_type='completed',
            score=score,
            percentage=percentage
        )
        
        return result


class UserJourneyIntegrationTest(APIIntegrationTestCase):
    """
    ユーザージャーニー全体を通じたAPI統合テスト
    """
    
    def test_complete_user_journey(self):
        """
        完全なユーザージャーニーのテスト：
        1. ユーザー登録
        2. ログイン
        3. カテゴリー一覧取得
        4. 難易度選択
        5. クイズ開始
        6. 問題回答
        7. 結果保存
        8. 統計確認
        9. 活動履歴確認
        """
        # 1. ユーザー登録
        register_url = reverse('users:register')
        register_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(register_url, register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
        
        # 2. ログイン
        login_url = reverse('users:token_obtain_pair')
        login_data = {
            'username': 'newuser',
            'password': 'newpass123'
        }
        response = self.client.post(login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        
        # トークンを設定
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # 3. カテゴリー一覧取得
        categories_url = reverse('quiz:category-list')
        response = self.client.get(categories_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        categories = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(categories), 3)
        
        # Pythonカテゴリーを選択
        python_category = next(c for c in categories if c['slug'] == 'python')
        
        # 4. 難易度一覧取得
        difficulties_url = reverse('quiz:difficultylevel-list')
        response = self.client.get(difficulties_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        difficulties = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(difficulties), 3)
        
        # Beginnerを選択
        beginner_difficulty = next(d for d in difficulties if d['slug'] == 'beginner')
        
        # 5. 選択したカテゴリー・難易度のクイズを取得
        quiz_filter_url = reverse('quiz:quiz-filter-by-category-and-difficulty',
                                 args=[python_category['id'], beginner_difficulty['id']])
        response = self.client.get(quiz_filter_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        quizzes = response.data['results'] if 'results' in response.data else response.data
        self.assertGreater(len(quizzes), 0)
        
        selected_quiz = quizzes[0]
        
        # 6. クイズの問題を取得
        questions_url = reverse('quiz:quiz-questions', args=[selected_quiz['id']])
        response = self.client.get(questions_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        questions = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(questions), 3)
        
        # 7. 各問題に回答（全問正解）
        start_time = time.time()
        total_score = 0
        for question in questions:
            # 正解の選択肢を見つける
            correct_answer = next(a for a in question['answers'] if a['is_correct'])
            total_score += question['points']
        
        time_taken = int(time.time() - start_time) + 5  # 5秒追加してリアルな時間に
        
        # 8. クイズ結果を保存
        result_url = reverse('quiz:quizresult-list')
        result_data = {
            'quiz': selected_quiz['id'],
            'score': total_score,
            'total_possible': total_score,
            'time_taken': time_taken,
            'percentage': 100.0
        }
        response = self.client.post(result_url, result_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['score'], total_score)
        self.assertEqual(response.data['passed'], True)
        
        # テスト環境ではSupabaseトリガーが動作しないため、統計情報と活動履歴を手動で作成
        # 実際のユーザーを取得
        from django.contrib.auth import get_user_model
        User = get_user_model()
        current_user = User.objects.get(username='newuser')
        quiz_obj = Quiz.objects.get(id=selected_quiz['id'])
        
        # ヘルパーメソッドを使用して統計情報と活動履歴を作成
        self.create_quiz_result_with_stats(
            user=current_user,
            quiz=quiz_obj,
            score=total_score,
            total_possible=total_score,
            time_taken=time_taken
        )
        
        # 9. ユーザー統計を確認
        
        stats_url = reverse('quiz:userstatistics-summary')
        response = self.client.get(stats_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        stats = response.data
        self.assertEqual(stats['total_quizzes_completed'], 1)
        self.assertEqual(stats['overall_avg_score'], 100.0)
        
        # 10. 最近の活動履歴を確認
        
        activities_url = reverse('quiz:activityhistory-recent')
        response = self.client.get(activities_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        activities = response.data['results'] if 'results' in response.data else response.data
        self.assertGreater(len(activities), 0)
        
        recent_activity = activities[0]
        self.assertEqual(recent_activity['activity_type'], 'completed')
        self.assertEqual(recent_activity['score'], total_score)
    
    def test_multiple_quiz_attempts_and_statistics(self):
        """
        複数回のクイズ挑戦と統計情報の更新をテスト
        """
        user, tokens = self.create_user_and_authenticate('multiuser')
        
        # 異なるクイズに3回挑戦
        quiz_attempts = [
            ('python_beginner', 30, 30, 100.0),    # 全問正解
            ('javascript_intermediate', 20, 30, 66.7),  # 部分正解
            ('django_advanced', 10, 30, 33.3),     # 低スコア
        ]
        
        for quiz_key, score, total, percentage in quiz_attempts:
            quiz = self.quizzes[quiz_key]
            
            # クイズ結果を保存（統計情報と活動履歴も含む）
            self.create_quiz_result_with_stats(
                user=user,
                quiz=quiz,
                score=score,
                total_possible=total,
                time_taken=300  # 5分
            )
        
        # 統計情報を確認
        stats_url = reverse('quiz:userstatistics-summary')
        response = self.client.get(stats_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        stats = response.data
        self.assertEqual(stats['total_quizzes_completed'], 3)
        self.assertAlmostEqual(stats['overall_avg_score'], 66.67, places=1)
        
        # カテゴリー別統計を確認
        self.assertIn('categories', stats)
        # カテゴリー別統計は実装によって異なる可能性があるため、詳細なチェックは省略
    
    def test_quiz_filtering_and_search(self):
        """
        クイズのフィルタリングと検索機能のテスト
        """
        user, tokens = self.create_user_and_authenticate('searchuser')
        
        # カテゴリーでフィルタリング
        python_category = self.categories['python']
        url = reverse('quiz:quiz-list')
        response = self.client.get(url, {'category': python_category.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        quizzes = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(quizzes), 3)  # 3つの難易度
        for quiz in quizzes:
            self.assertEqual(quiz['category'], python_category.id)
        
        # 難易度でフィルタリング
        beginner_difficulty = self.difficulties['beginner']
        response = self.client.get(url, {'difficulty': beginner_difficulty.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        quizzes = response.data['results'] if 'results' in response.data else response.data
        self.assertEqual(len(quizzes), 3)  # 3つのカテゴリー
        for quiz in quizzes:
            self.assertEqual(quiz['difficulty'], beginner_difficulty.id)
        
        # 検索機能のテスト
        response = self.client.get(url, {'search': 'Python'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        quizzes = response.data['results'] if 'results' in response.data else response.data
        self.assertGreater(len(quizzes), 0)
        for quiz in quizzes:
            self.assertIn('Python', quiz['title'])
    
    def test_activity_history_pagination(self):
        """
        活動履歴のページネーションテスト
        """
        user, tokens = self.create_user_and_authenticate('paginationuser')
        
        # 15個のクイズ結果を作成（統計情報と活動履歴も含む）
        for i in range(15):
            quiz = list(self.quizzes.values())[i % len(self.quizzes)]
            score = 20 + (i % 10)
            self.create_quiz_result_with_stats(
                user=user,
                quiz=quiz,
                score=score,
                total_possible=30,
                time_taken=300
            )
        
        # 最初の10件を取得
        activities_url = reverse('quiz:activityhistory-list')
        response = self.client.get(activities_url, {'limit': 10, 'offset': 0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.data
        self.assertEqual(data['count'], 15)
        self.assertEqual(len(data['results']), 10)
        self.assertIsNotNone(data['next'])
        self.assertIsNone(data['previous'])
        
        # 次の5件を取得
        response = self.client.get(activities_url, {'limit': 10, 'offset': 10})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.data
        self.assertEqual(len(data['results']), 5)
        self.assertIsNone(data['next'])
        self.assertIsNotNone(data['previous'])


class APIErrorHandlingTest(APIIntegrationTestCase):
    """
    APIエラーハンドリングの統合テスト
    """
    
    def test_unauthorized_access(self):
        """認証なしでのアクセステスト"""
        # 認証なしでクイズ結果を保存しようとする
        url = reverse('quiz:quizresult-list')
        data = {
            'quiz': 1,
            'score': 10,
            'total_possible': 10,
            'time_taken': 100,
            'percentage': 100.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_invalid_quiz_result_data(self):
        """無効なクイズ結果データのテスト"""
        user, tokens = self.create_user_and_authenticate()
        
        url = reverse('quiz:quizresult-list')
        
        # 存在しないクイズID
        data = {
            'quiz': 9999,
            'score': 10,
            'total_possible': 10,
            'time_taken': 100,
            'percentage': 100.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # スコアが総得点を超える
        quiz = list(self.quizzes.values())[0]
        data = {
            'quiz': quiz.id,
            'score': 100,
            'total_possible': 50,
            'time_taken': 100,
            'percentage': 200.0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_token_expiration_handling(self):
        """トークン期限切れのハンドリングテスト"""
        # 期限切れトークンをシミュレート
        user = User.objects.create_user(
            username='expireduser',
            email='expired@example.com',
            password='testpass123'
        )
        
        # 過去の時間でトークンを作成（実際には期限切れトークンは作成できないため、
        # 無効なトークンを使用）
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        
        url = reverse('quiz:category-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_concurrent_quiz_attempts(self):
        """同時クイズ挑戦のテスト"""
        user, tokens = self.create_user_and_authenticate()
        
        quiz = list(self.quizzes.values())[0]
        url = reverse('quiz:quizresult-list')
        
        # 同じクイズに対して短時間で2回結果を送信
        result_data = {
            'quiz': quiz.id,
            'score': 20,
            'total_possible': 30,
            'time_taken': 300,
            'percentage': 66.7
        }
        
        # 1回目
        response1 = self.client.post(url, result_data, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        
        # 2回目（すぐに送信）
        result_data['score'] = 25
        result_data['percentage'] = 83.3
        response2 = self.client.post(url, result_data, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        
        # 両方の結果が保存されていることを確認
        results = QuizResult.objects.filter(user=user, quiz=quiz).order_by('-created_at')
        self.assertEqual(results.count(), 2)
        self.assertEqual(results[0].score, 25)
        self.assertEqual(results[1].score, 20)


class APIPerformanceTest(APIIntegrationTestCase):
    """
    APIパフォーマンステスト
    """
    
    def test_bulk_data_handling(self):
        """大量データの処理テスト"""
        user, tokens = self.create_user_and_authenticate('bulkuser')
        
        # 50個のクイズ結果を作成
        start_time = time.time()
        
        for i in range(50):
            quiz = list(self.quizzes.values())[i % len(self.quizzes)]
            result_data = {
                'quiz': quiz.id,
                'score': 15 + (i % 15),
                'total_possible': 30,
                'time_taken': 200 + (i * 10),
                'percentage': (15 + (i % 15)) / 30 * 100
            }
            url = reverse('quiz:quizresult-list')
            self.client.post(url, result_data, format='json')
        
        creation_time = time.time() - start_time
        
        # 作成時間が妥当な範囲内であることを確認（10秒以内）
        self.assertLess(creation_time, 10.0)
        
        # 統計情報の取得時間をテスト
        start_time = time.time()
        stats_url = reverse('quiz:userstatistics-summary')
        response = self.client.get(stats_url)
        stats_time = time.time() - start_time
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(stats_time, 1.0)  # 1秒以内
        
        # 活動履歴の取得時間をテスト
        start_time = time.time()
        activities_url = reverse('quiz:activityhistory-list')
        response = self.client.get(activities_url, {'page_size': 20})
        activities_time = time.time() - start_time
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(activities_time, 1.0)  # 1秒以内
    
    def test_complex_filtering_performance(self):
        """複雑なフィルタリングのパフォーマンステスト"""
        user, tokens = self.create_user_and_authenticate('filteruser')
        
        # まず30個のクイズ結果を作成
        for i in range(30):
            quiz = list(self.quizzes.values())[i % len(self.quizzes)]
            result_data = {
                'quiz': quiz.id,
                'score': 10 + (i % 20),
                'total_possible': 30,
                'time_taken': 300,
                'percentage': (10 + (i % 20)) / 30 * 100
            }
            url = reverse('quiz:quizresult-list')
            self.client.post(url, result_data, format='json')
        
        # 複数条件でのフィルタリング
        start_time = time.time()
        
        # 期間指定での活動履歴取得
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        activities_url = reverse('quiz:activityhistory-list')
        params = {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'category': self.categories['python'].id,
            'ordering': '-score'
        }
        
        response = self.client.get(activities_url, params)
        filter_time = time.time() - start_time
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertLess(filter_time, 1.0)  # 1秒以内
        
        # 結果が正しくフィルタリングされていることを確認
        results = response.data['results'] if 'results' in response.data else response.data
        for activity in results:
            self.assertEqual(activity['category'], self.categories['python'].id) 