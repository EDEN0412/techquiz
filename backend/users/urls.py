from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, 
    RegisterView,
    CustomTokenObtainPairView
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
    TokenBlacklistView,
)

app_name = 'users'

# ViewSetをルーターに登録
router = DefaultRouter()
router.register(r'', UserViewSet)  # 'users'を削除して空文字列に変更

urlpatterns = [
    # ユーザー登録エンドポイント
    path('register/', RegisterView.as_view(), name='register'),
    
    # JWT認証エンドポイント
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # ログアウトエンドポイント（リフレッシュトークンを無効化）
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
    
    # ルーターが生成したURLパターンを含める（最後に配置）
    path('', include(router.urls)),
] 