from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse


class UserProfileModelTest(TestCase):
    """UserProfileモデルのテスト"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com',
            password='testpassword123'
        )
    
    def test_profile_creation(self):
        """ユーザー作成時にプロフィールが自動的に作成されることを確認"""
        self.assertIsNotNone(self.user.profile)
        self.assertTrue(isinstance(self.user.profile, UserProfile))
        self.assertEqual(self.user.profile.user, self.user)
    
    def test_profile_str_representation(self):
        """プロフィールの文字列表現が期待通りであることを確認"""
        expected_string = f"{self.user.username}'s profile"
        self.assertEqual(str(self.user.profile), expected_string)


class UserAPITest(APITestCase):
    """ユーザーAPI関連のテスト"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com',
            password='testpassword123'
        )
        
        # ユーザー登録用データ
        self.valid_register_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newuserpassword123',
            'password2': 'newuserpassword123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        # ログイン用データ
        self.login_data = {
            'username': 'testuser',
            'password': 'testpassword123'
        }
    
    def test_user_registration(self):
        """ユーザー登録APIが正常に動作することを確認"""
        url = reverse('users:register')
        response = self.client.post(url, self.valid_register_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_token_obtain(self):
        """トークン取得APIが正常に動作することを確認"""
        url = reverse('users:token_obtain_pair')
        response = self.client.post(url, self.login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    def test_me_endpoint_authenticated(self):
        """認証済みユーザーが/me/エンドポイントにアクセスできることを確認"""
        # 先にログインしてトークンを取得
        token_url = reverse('users:token_obtain_pair')
        token_response = self.client.post(token_url, self.login_data, format='json')
        token = token_response.data['access']
        
        # 認証ヘッダーをセット
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        
        # /me/エンドポイントにアクセス
        url = reverse('users:user-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
    
    def test_me_endpoint_unauthenticated(self):
        """未認証ユーザーが/me/エンドポイントにアクセスできないことを確認"""
        url = reverse('users:user-me')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 