"""
難易度モデル
"""

from django.db import models
from django.utils.text import slugify
from techskillsquiz.supabase_mixins import SupabaseModelMixin


class DifficultyLevel(models.Model, SupabaseModelMixin):
    """
    クイズの難易度レベルモデル
    """
    supabase_table = 'quiz_difficultylevel'

    name = models.CharField('難易度名', max_length=50)
    slug = models.SlugField('スラッグ', max_length=50, unique=True)
    level = models.PositiveSmallIntegerField('レベル値', unique=True)
    description = models.TextField('説明', blank=True)
    point_multiplier = models.PositiveIntegerField('ポイント倍率', default=1)
    time_limit = models.PositiveIntegerField('制限時間（秒）', default=600)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = '難易度'
        verbose_name_plural = '難易度'
        ordering = ['level']

    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        # スラッグが設定されていない場合、名前から自動生成
        if not self.slug:
            self.slug = slugify(self.name)
            
            # 同じスラッグが既に存在する場合、数字を追加して一意にする
            original_slug = self.slug
            counter = 1
            while DifficultyLevel.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
                
        super().save(*args, **kwargs) 