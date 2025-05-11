"""
クイズアプリのビューに対するテスト
"""

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from quiz.models import Category

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