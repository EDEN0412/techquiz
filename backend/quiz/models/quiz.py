"""
クイズモデル
"""

from django.db import models
from techskillsquiz.supabase_mixins import SupabaseModelMixin
from .category import Category
from .difficulty import DifficultyLevel


class Quiz(models.Model, SupabaseModelMixin):
    """
    クイズモデル - カテゴリと難易度に関連付けられたクイズ
    """
    supabase_table = 'quiz_quiz'

    category = models.ForeignKey(
        Category, 
        verbose_name='カテゴリ',
        on_delete=models.CASCADE, 
        related_name='quizzes'
    )
    difficulty = models.ForeignKey(
        DifficultyLevel, 
        verbose_name='難易度',
        on_delete=models.CASCADE, 
        related_name='quizzes'
    )
    title = models.CharField('タイトル', max_length=200)
    description = models.TextField('説明', blank=True)
    time_limit = models.PositiveIntegerField('制限時間（秒）', default=600)
    pass_score = models.PositiveIntegerField('合格点', default=70)
    is_active = models.BooleanField('アクティブ状態', default=True)
    thumbnail_url = models.URLField('サムネイル画像URL', blank=True)
    banner_image_url = models.URLField('バナー画像URL', blank=True)
    media_type = models.CharField('メディア種類', max_length=50, blank=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = 'クイズ'
        verbose_name_plural = 'クイズ'
        ordering = ['category', 'difficulty', 'title']

    def __str__(self):
        return f"{self.title} ({self.category.name} - {self.difficulty.name})" 