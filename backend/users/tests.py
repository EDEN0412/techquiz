from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken


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

        # パスワード変更用データ
        self.password_change_data = {
            'old_password': 'testpassword123',
            'new_password': 'newstrongpassword456'
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

    def test_token_refresh(self):
        """リフレッシュトークンを使用して新しいアクセストークンを取得できることを確認"""
        # 先にログインしてトークンを取得
        token_url = reverse('users:token_obtain_pair')
        token_response = self.client.post(token_url, self.login_data, format='json')
        refresh_token = token_response.data['refresh']
        
        # リフレッシュトークンを使用して新しいアクセストークンを取得
        refresh_url = reverse('users:token_refresh')
        refresh_data = {'refresh': refresh_token}
        response = self.client.post(refresh_url, refresh_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        
        # 新しいアクセストークンが有効か確認
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {response.data["access"]}')
        me_url = reverse('users:user-me')
        me_response = self.client.get(me_url)
        self.assertEqual(me_response.status_code, status.HTTP_200_OK)
    
    def test_token_verify(self):
        """トークン検証エンドポイントが正常に動作することを確認"""
        # 先にログインしてトークンを取得
        token_url = reverse('users:token_obtain_pair')
        token_response = self.client.post(token_url, self.login_data, format='json')
        access_token = token_response.data['access']
        
        # アクセストークンを検証
        verify_url = reverse('users:token_verify')
        verify_data = {'token': access_token}
        response = self.client.post(verify_url, verify_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 無効なトークンでの検証も確認
        invalid_data = {'token': 'invalid_token'}
        invalid_response = self.client.post(verify_url, invalid_data, format='json')
        self.assertEqual(invalid_response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_logout(self):
        """ログアウト（リフレッシュトークンの無効化）が正常に動作することを確認"""
        # 先にログインしてトークンを取得
        token_url = reverse('users:token_obtain_pair')
        token_response = self.client.post(token_url, self.login_data, format='json')
        refresh_token = token_response.data['refresh']
        
        # ログアウト（リフレッシュトークンを無効化）
        logout_url = reverse('users:token_blacklist')
        logout_data = {'refresh': refresh_token}
        response = self.client.post(logout_url, logout_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 無効化後のリフレッシュトークンは使用できないことを確認
        refresh_url = reverse('users:token_refresh')
        refresh_data = {'refresh': refresh_token}
        refresh_response = self.client.post(refresh_url, refresh_data, format='json')
        
        self.assertEqual(refresh_response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_change_password(self):
        """パスワード変更APIが正常に動作することを確認"""
        # 先にログインしてトークンを取得
        token_url = reverse('users:token_obtain_pair')
        token_response = self.client.post(token_url, self.login_data, format='json')
        access_token = token_response.data['access']
        
        # 認証ヘッダーをセット
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # パスワード変更
        url = reverse('users:user-change-password')
        response = self.client.put(url, self.password_change_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 古いパスワードでのログインが失敗することを確認
        old_login_response = self.client.post(token_url, self.login_data, format='json')
        self.assertEqual(old_login_response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # 新しいパスワードでのログインが成功することを確認
        new_login_data = {
            'username': 'testuser',
            'password': 'newstrongpassword456'
        }
        new_login_response = self.client.post(token_url, new_login_data, format='json')
        self.assertEqual(new_login_response.status_code, status.HTTP_200_OK)
        self.assertIn('access', new_login_response.data)
    
    def test_change_password_invalid_old_password(self):
        """間違った古いパスワードでパスワード変更が失敗することを確認"""
        # 先にログインしてトークンを取得
        token_url = reverse('users:token_obtain_pair')
        token_response = self.client.post(token_url, self.login_data, format='json')
        access_token = token_response.data['access']
        
        # 認証ヘッダーをセット
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        # 間違った古いパスワードでパスワード変更
        invalid_data = {
            'old_password': 'wrongpassword',
            'new_password': 'newstrongpassword456'
        }
        url = reverse('users:user-change-password')
        response = self.client.put(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST) 