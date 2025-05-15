from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, 
    UserProfileViewSet, 
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
router.register(r'users', UserViewSet)
router.register(r'profiles', UserProfileViewSet)

urlpatterns = [
    # ルーターが生成したURLパターンを含める
    path('', include(router.urls)),
    
    # ユーザー登録エンドポイント
    path('register/', RegisterView.as_view(), name='register'),
    
    # JWT認証エンドポイント
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # ログアウトエンドポイント（リフレッシュトークンを無効化）
    path('logout/', TokenBlacklistView.as_view(), name='token_blacklist'),
] 