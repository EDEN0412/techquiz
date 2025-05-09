"""
クイズアプリのURL設定
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    DifficultyLevelViewSet,
    QuizViewSet,
    QuestionViewSet,
    AnswerViewSet,
    QuizResultViewSet,
    UserStatisticsViewSet,
    ActivityHistoryViewSet
)

# DRF用ルーターの初期化
router = DefaultRouter()

# 各ViewSetをルーターに登録
router.register(r'categories', CategoryViewSet)
router.register(r'difficulty-levels', DifficultyLevelViewSet)
router.register(r'quizzes', QuizViewSet)
router.register(r'questions', QuestionViewSet)
router.register(r'answers', AnswerViewSet)
router.register(r'quiz-results', QuizResultViewSet)
router.register(r'user-statistics', UserStatisticsViewSet)
router.register(r'activity-history', ActivityHistoryViewSet)

# アプリのURLパターン
urlpatterns = [
    # ルーターで生成されたURLを含める
    path('', include(router.urls)),
]

# エクスポートするURLパターン名
app_name = 'quiz' 