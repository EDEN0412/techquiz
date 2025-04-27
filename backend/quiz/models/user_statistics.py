"""
ユーザー統計情報モデル
"""

from django.db import models
from django.contrib.auth import get_user_model
from techskillsquiz.supabase_mixins import SupabaseModelMixin
from .category import Category
from .difficulty import DifficultyLevel

User = get_user_model()


class UserStatistics(models.Model, SupabaseModelMixin):
    """
    ユーザー統計情報モデル - ユーザーのクイズ活動に関する統計データ
    """
    supabase_table = 'quiz_userstatistics'

    user = models.ForeignKey(
        User, 
        verbose_name='ユーザー',
        on_delete=models.CASCADE, 
        related_name='statistics'
    )
    category = models.ForeignKey(
        Category, 
        verbose_name='カテゴリ',
        on_delete=models.SET_NULL, 
        related_name='user_statistics',
        null=True,
        blank=True
    )
    difficulty = models.ForeignKey(
        DifficultyLevel, 
        verbose_name='難易度',
        on_delete=models.SET_NULL, 
        related_name='user_statistics',
        null=True,
        blank=True
    )
    quizzes_completed = models.PositiveIntegerField('完了クイズ数', default=0)
    total_points = models.PositiveIntegerField('合計ポイント', default=0)
    avg_score = models.FloatField('平均スコア', default=0.0)
    highest_score = models.PositiveIntegerField('最高スコア', default=0)
    last_quiz_date = models.DateTimeField('最終クイズ日', null=True, blank=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = 'ユーザー統計'
        verbose_name_plural = 'ユーザー統計'
        ordering = ['user', 'category', 'difficulty']
        unique_together = [
            ['user', 'category', 'difficulty']
        ]
        indexes = [
            models.Index(fields=['user', 'category']),
            models.Index(fields=['user', 'difficulty']),
        ]

    def __str__(self):
        category_name = self.category.name if self.category else "全カテゴリ"
        difficulty_name = self.difficulty.name if self.difficulty else "全難易度"
        return f"{self.user.username} - {category_name} - {difficulty_name} - 完了: {self.quizzes_completed}回, 平均: {self.avg_score:.1f}%" 