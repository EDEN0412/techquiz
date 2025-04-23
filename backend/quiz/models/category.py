"""
カテゴリモデル
"""

from django.db import models
from techskillsquiz.supabase_mixins import SupabaseModelMixin


class Category(models.Model, SupabaseModelMixin):
    """
    クイズのカテゴリモデル
    """
    supabase_table = 'quiz_category'

    name = models.CharField('カテゴリ名', max_length=100)
    slug = models.SlugField('スラッグ', max_length=100, unique=True)
    description = models.TextField('説明', blank=True)
    icon = models.CharField('アイコン', max_length=50, blank=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = 'カテゴリ'
        verbose_name_plural = 'カテゴリ'
        ordering = ['name']

    def __str__(self):
        return self.name 