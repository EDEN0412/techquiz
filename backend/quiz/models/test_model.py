"""
テスト用のSupabaseモデル
"""

from django.db import models
from techskillsquiz.supabase_mixins import SupabaseModelMixin


class TestSupabaseModel(models.Model, SupabaseModelMixin):
    """
    Supabase同期のテスト用モデル
    """
    supabase_table = 'quiz_testsupabasemodel'
    
    name = models.CharField(max_length=100, verbose_name='名前')
    description = models.TextField(blank=True, null=True, verbose_name='説明')
    is_active = models.BooleanField(default=True, verbose_name='有効')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='作成日時')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新日時')
    
    class Meta:
        verbose_name = 'テストモデル'
        verbose_name_plural = 'テストモデル'
        
    def __str__(self):
        return self.name 