"""
ユーザー活動履歴モデル
"""

from django.db import models
from django.contrib.auth import get_user_model
from techskillsquiz.supabase_mixins import SupabaseModelMixin
from .quiz import Quiz
from .category import Category
from .difficulty import DifficultyLevel

User = get_user_model()


class ActivityHistory(models.Model, SupabaseModelMixin):
    """
    ユーザー活動履歴モデル - ユーザーのクイズ活動履歴を記録
    """
    supabase_table = 'quiz_activityhistory'

    ACTIVITY_TYPES = (
        ('quiz_completed', 'クイズ完了'),
        ('quiz_started', 'クイズ開始'),
        ('quiz_review', 'クイズ復習'),
        ('achievement_earned', '実績獲得'),
    )

    user = models.ForeignKey(
        User, 
        verbose_name='ユーザー',
        on_delete=models.CASCADE, 
        related_name='activity_history'
    )
    quiz = models.ForeignKey(
        Quiz, 
        verbose_name='クイズ',
        on_delete=models.CASCADE, 
        related_name='activity_history'
    )
    category = models.ForeignKey(
        Category, 
        verbose_name='カテゴリ',
        on_delete=models.SET_NULL, 
        related_name='activity_history',
        null=True
    )
    difficulty = models.ForeignKey(
        DifficultyLevel, 
        verbose_name='難易度',
        on_delete=models.SET_NULL, 
        related_name='activity_history',
        null=True
    )
    score = models.PositiveIntegerField('スコア', default=0)
    percentage = models.FloatField('正答率', default=0.0)
    activity_date = models.DateTimeField('活動日時', auto_now_add=True)
    activity_type = models.CharField(
        '活動タイプ', 
        max_length=20, 
        choices=ACTIVITY_TYPES, 
        default='quiz_completed'
    )
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = '活動履歴'
        verbose_name_plural = '活動履歴'
        ordering = ['-activity_date']
        indexes = [
            models.Index(fields=['user', '-activity_date']),
            models.Index(fields=['user', 'category']),
            models.Index(fields=['user', 'activity_type']),
        ]

    def __str__(self):
        activity = dict(self.ACTIVITY_TYPES).get(self.activity_type, self.activity_type)
        return f"{self.user.username} - {activity} - {self.quiz.title} - {self.score}点 ({self.percentage:.1f}%)" 