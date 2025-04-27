"""
クイズの問題モデル
"""

from django.db import models
from techskillsquiz.supabase_mixins import SupabaseModelMixin
from .quiz import Quiz


class Question(models.Model, SupabaseModelMixin):
    """
    クイズの問題モデル - 各クイズに含まれる個別の問題
    """
    supabase_table = 'quiz_question'

    QUESTION_TYPES = (
        ('single_choice', '単一選択'),
        ('multiple_choice', '複数選択'),
        ('true_false', '正誤問題'),
        ('fill_blank', '穴埋め'),
        ('code_snippet', 'コード記述'),
    )

    MEDIA_TYPES = (
        ('none', 'なし'),
        ('code', 'コード'),
        ('image', '画像'),
        ('diagram', '図表'),
    )

    quiz = models.ForeignKey(
        Quiz, 
        verbose_name='クイズ',
        on_delete=models.CASCADE, 
        related_name='questions'
    )
    question_text = models.TextField('問題文')
    question_type = models.CharField(
        '問題タイプ', 
        max_length=20, 
        choices=QUESTION_TYPES, 
        default='single_choice'
    )
    hint = models.TextField('ヒント', blank=True)
    explanation = models.TextField('解説', blank=True)
    points = models.PositiveIntegerField('ポイント', default=10)
    display_order = models.PositiveIntegerField('表示順序', default=0)
    code_snippet = models.TextField('コードスニペット', blank=True)
    image_url = models.URLField('画像URL', blank=True)
    media_type = models.CharField(
        'メディアタイプ', 
        max_length=10, 
        choices=MEDIA_TYPES, 
        default='none'
    )
    syntax_highlight = models.CharField('シンタックスハイライト言語', max_length=30, blank=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = '問題'
        verbose_name_plural = '問題'
        ordering = ['quiz', 'display_order']

    def __str__(self):
        return f"{self.quiz.title} - 問題{self.display_order}: {self.question_text[:30]}..." 