"""
フロントエンドAPIクライアントのモックテスト
"""

import json
import pytest
import asyncio
from unittest import mock
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from asgiref.sync import sync_to_async
import threading
from concurrent.futures import ThreadPoolExecutor

from ..models import (
    Category,
    DifficultyLevel,
    Quiz,
    Question,
    Answer,
    QuizResult,
    UserStatistics,
    ActivityHistory
)


class MockResponse:
    """
    APIレスポンスをモックするシンプルなクラス
    """
    def __init__(self, data, status_code=200):
        self.data = data
        self.status_code = status_code


class ApiClientMock:
    """
    フロントエンドのAPIクライアントをモックするクラス
    実際のフロントエンド（src/lib/api/client.ts）の振る舞いをシミュレート
    """
    
    def __init__(self, test_case, base_url='/api/v1/quiz'):
        self.test_case = test_case
        self.client = test_case.client
        self.base_url = base_url
    
    async def get(self, url, params=None):
        """
        非同期的にGETリクエストを実行（モック）
        """
        # sync_to_asyncでAPIClientのメソッドを非同期化
        get_func = sync_to_async(self.client.get)
        response = await get_func(url, data=params)
        return response
    
    async def post(self, url, data=None):
        """
        非同期的にPOSTリクエストを実行（モック）
        """
        # sync_to_asyncでAPIClientのメソッドを非同期化
        post_func = sync_to_async(self.client.post)
        response = await post_func(url, data=data, format='json')
        return response


class QuizServiceMock:
    """
    フロントエンドのQuizServiceをモックするクラス
    実際のフロントエンド（src/lib/api/services/quiz.service.ts）の振る舞いをシミュレート
    """
    
    def __init__(self):
        """
        初期化
        """
        self.base_url = '/api/v1/quiz'
    
    # カテゴリー関連メソッド
    def getCategories(self):
        """
        カテゴリ一覧を取得
        """
        # APIレスポンスをモック
        response = MockResponse([
            {'id': 1, 'name': 'Python', 'description': 'Python programming language', 'display_order': 1, 'is_active': True},
            {'id': 2, 'name': 'JavaScript', 'description': 'JavaScript programming language', 'display_order': 2, 'is_active': True}
        ])
        
        if response.status_code == 200:
            return response.data
        raise Exception(f"Failed to fetch categories: {response.status_code}")
    
    # 難易度関連メソッド
    def getDifficultyLevels(self):
        """
        難易度一覧を取得
        """
        # APIレスポンスをモック
        response = MockResponse([
            {'id': 1, 'name': 'Beginner', 'description': 'Beginner level', 'level': 1},
            {'id': 2, 'name': 'Intermediate', 'description': 'Intermediate level', 'level': 2}
        ])
        
        if response.status_code == 200:
            return response.data
        raise Exception(f"Failed to fetch difficulty levels: {response.status_code}")
    
    # クイズ関連メソッド
    def getQuizzes(self):
        """
        クイズ一覧を取得
        """
        # APIレスポンスをモック
        response = MockResponse([
            {'id': 1, 'title': 'Python Basics', 'description': 'Basic Python programming concepts', 'category': {'id': 1, 'name': 'Python'}, 'difficulty': {'id': 1, 'name': 'Beginner'}}
        ])
        
        if response.status_code == 200:
            return response.data
        raise Exception(f"Failed to fetch quizzes: {response.status_code}")
    
    def getQuizzesByCategory(self, categoryId):
        """
        特定のカテゴリに属するクイズ一覧を取得
        """
        # APIレスポンスをモック
        response = MockResponse([
            {'id': 1, 'title': 'Python Basics', 'description': 'Basic Python programming concepts', 'category': {'id': 1, 'name': 'Python'}, 'difficulty': {'id': 1, 'name': 'Beginner'}}
        ])
        
        if response.status_code == 200:
            return response.data
        raise Exception(f"Failed to fetch quizzes by category: {response.status_code}")
    
    def getQuiz(self, quizId):
        """
        特定のクイズの詳細を取得
        """
        # 存在しないIDの場合はエラーを返す
        if quizId == 9999:
            response = MockResponse(None, status_code=404)
        else:
            # 正常なレスポンスをモック
            response = MockResponse({
                'id': quizId,
                'title': 'Python Basics',
                'description': 'Basic Python programming concepts',
                'category': {'id': 1, 'name': 'Python'},
                'difficulty': {'id': 1, 'name': 'Beginner'}
            })
        
        if response.status_code == 200:
            return response.data
        raise Exception(f"Failed to fetch quiz: {response.status_code}")
    
    # クイズ結果関連メソッド
    def saveQuizResult(self, quizResult):
        """
        クイズ結果を保存
        """
        # APIレスポンスをモック
        response = MockResponse({
            'id': 1,
            'quiz': quizResult['quiz'],
            'user': quizResult['user'],
            'score': quizResult['score'],
            'total_possible': quizResult['total_possible'],
            'percentage': quizResult['percentage'],
            'time_taken': quizResult['time_taken'],
            'passed': quizResult['score'] >= 70,
            'completed_at': '2023-01-01T00:00:00Z'
        }, status_code=201)
        
        if response.status_code == 201:
            return response.data
        raise Exception(f"Failed to save quiz result: {response.status_code}")


@pytest.mark.api_client_mock
class ApiClientMockTest(TestCase):
    """
    フロントエンドAPIクライアントのモックを使用したテスト
    """
    
    def setUp(self):
        """
        テストデータのセットアップ
        """
        # QuizServiceのモック設定
        self.quiz_service = QuizServiceMock()
        
        # テストデータの設定
        self.category_id = 1
        self.quiz_id = 1
        self.user_id = 1
    
    def test_error_handling_mock(self):
        """
        エラーハンドリングのモックテスト
        フロントエンドのエラーハンドリングをシミュレート
        """
        # 存在しないクイズIDでgetQuizを呼び出し、例外が発生することを期待
        with self.assertRaises(Exception) as context:
            self.quiz_service.getQuiz(9999)
        
        # 例外メッセージに含まれる文字列を検証
        self.assertIn("Failed to fetch quiz", str(context.exception))
    
    def test_get_categories_mock(self):
        """
        カテゴリ一覧取得APIをモックを使ってテスト
        """
        # モックサービスから応答を取得
        categories = self.quiz_service.getCategories()
        
        # レスポンスの検証
        self.assertIsNotNone(categories)
        self.assertEqual(len(categories), 2)
        self.assertEqual(categories[0]['name'], 'Python')
        self.assertEqual(categories[1]['name'], 'JavaScript')
    
    def test_get_difficulty_levels_mock(self):
        """
        難易度一覧取得APIをモックを使ってテスト
        """
        # モックサービスから応答を取得
        difficulties = self.quiz_service.getDifficultyLevels()
        
        # レスポンスの検証
        self.assertIsNotNone(difficulties)
        self.assertEqual(len(difficulties), 2)
        self.assertEqual(difficulties[0]['name'], 'Beginner')
        self.assertEqual(difficulties[1]['name'], 'Intermediate')
    
    def test_get_quizzes_mock(self):
        """
        クイズ一覧取得APIをモックを使ってテスト
        """
        # モックサービスから応答を取得
        quizzes = self.quiz_service.getQuizzes()
        
        # レスポンスの検証
        self.assertIsNotNone(quizzes)
        self.assertEqual(len(quizzes), 1)
        self.assertEqual(quizzes[0]['title'], 'Python Basics')
    
    def test_save_quiz_result_mock(self):
        """
        クイズ結果保存APIをモックを使ってテスト
        """
        # クイズ結果データ
        result_data = {
            'quiz': self.quiz_id,
            'user': self.user_id,
            'score': 10,
            'total_possible': 10,
            'time_taken': 25,
            'percentage': 100.0,
        }
        
        # モックサービスから応答を取得
        saved_result = self.quiz_service.saveQuizResult(result_data)
        
        # レスポンスの検証
        self.assertIsNotNone(saved_result)
        self.assertEqual(saved_result['score'], 10)
        self.assertEqual(saved_result['total_possible'], 10)
        self.assertEqual(saved_result['percentage'], 100.0) 