"""
カテゴリモデル
"""

from django.db import models
from django.utils.text import slugify
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
    display_order = models.PositiveIntegerField('表示順序', default=0)
    is_active = models.BooleanField('アクティブ状態', default=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = 'カテゴリ'
        verbose_name_plural = 'カテゴリ'
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name
        
    def save(self, *args, **kwargs):
        # スラッグが設定されていない場合、名前から自動生成
        if not self.slug:
            self.slug = slugify(self.name)
            
            # 同じスラッグが既に存在する場合、数字を追加して一意にする
            original_slug = self.slug
            counter = 1
            while Category.objects.filter(slug=self.slug).exists():
                self.slug = f"{original_slug}-{counter}"
                counter += 1
        
        # オリジナルのsaveメソッドを呼び出し、Djangoモデルを保存
        # post_saveシグナルがトリガーされ、Supabaseテーブルに同期される
        super().save(*args, **kwargs) 