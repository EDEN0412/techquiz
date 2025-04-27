"""
問題の回答モデル
"""

from django.db import models
from techskillsquiz.supabase_mixins import SupabaseModelMixin
from .question import Question


class Answer(models.Model, SupabaseModelMixin):
    """
    問題の回答モデル - 各問題に対する選択肢や正解情報
    """
    supabase_table = 'quiz_answer'

    question = models.ForeignKey(
        Question, 
        verbose_name='問題',
        on_delete=models.CASCADE, 
        related_name='answers'
    )
    answer_text = models.TextField('回答テキスト')
    is_correct = models.BooleanField('正解フラグ', default=False)
    feedback = models.TextField('フィードバック', blank=True)
    display_order = models.PositiveIntegerField('表示順序', default=0)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = '回答'
        verbose_name_plural = '回答'
        ordering = ['question', 'display_order']

    def __str__(self):
        correct_mark = "✓" if self.is_correct else "✗"
        return f"{self.question.quiz.title} - 問題{self.question.display_order} - 回答: {self.answer_text[:20]}... [{correct_mark}]" 