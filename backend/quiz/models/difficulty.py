"""
難易度モデル
"""

from django.db import models
from techskillsquiz.supabase_mixins import SupabaseModelMixin


class DifficultyLevel(models.Model, SupabaseModelMixin):
    """
    クイズの難易度レベルモデル
    """
    supabase_table = 'difficulty_levels'

    name = models.CharField('難易度名', max_length=50)
    slug = models.SlugField('スラッグ', max_length=50, unique=True)
    level = models.PositiveSmallIntegerField('レベル値', unique=True)
    description = models.TextField('説明', blank=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = '難易度'
        verbose_name_plural = '難易度'
        ordering = ['level']

    def __str__(self):
        return self.name 