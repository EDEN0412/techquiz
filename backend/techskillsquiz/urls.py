"""
URL configuration for techskillsquiz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from django.http import JsonResponse

# Swagger APIドキュメント設定
schema_view = get_schema_view(
    openapi.Info(
        title="TechSkillsQuiz API",
        default_version='v1',
        description="TechSkillsQuiz Backend API Documentation",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# APIヘルスチェック用ビュー関数
def health_check(request):
    """
    APIヘルスチェック用のエンドポイント。
    サーバーが正常に動作していることを確認するために使用。
    """
    return JsonResponse({
        'status': 'healthy', 
        'message': 'API server is running'
    })

urlpatterns = [
    path("admin/", admin.site.urls),
    
    # ヘルスチェックエンドポイント
    path('health/', health_check, name='health_check'),
    
    # REST Framework API ブラウザUI
    path('api-auth/', include('rest_framework.urls')),
    
    # JWT認証エンドポイント
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # APIドキュメント
    # path('docs/', include_docs_urls(title='TechSkillsQuiz API')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    # アプリケーション別API
    path('api/v1/', include([
        # 今後、以下のようにアプリごとのURLsを追加していく
        # path('users/', include('users.urls')),
        path('quiz/', include('quiz.urls')),
    ])),
    
    # 直接アクセスできるようにするショートカット
    path('api/quiz/', include('quiz.urls')),
]
