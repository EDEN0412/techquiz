"""
クイズ結果モデル
"""

from django.db import models
from django.contrib.auth import get_user_model
from techskillsquiz.supabase_mixins import SupabaseModelMixin
from .quiz import Quiz

User = get_user_model()


class QuizResult(models.Model, SupabaseModelMixin):
    """
    クイズ結果モデル - ユーザーがクイズを完了した際の結果情報
    """
    supabase_table = 'quiz_quizresult'

    user = models.ForeignKey(
        User, 
        verbose_name='ユーザー',
        on_delete=models.CASCADE, 
        related_name='quiz_results'
    )
    quiz = models.ForeignKey(
        Quiz, 
        verbose_name='クイズ',
        on_delete=models.CASCADE, 
        related_name='results'
    )
    score = models.PositiveIntegerField('スコア')
    total_possible = models.PositiveIntegerField('満点')
    percentage = models.FloatField('正答率')
    time_taken = models.PositiveIntegerField('所要時間（秒）')
    passed = models.BooleanField('合格フラグ', default=False)
    completed_at = models.DateTimeField('完了日時', auto_now_add=True)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = 'クイズ結果'
        verbose_name_plural = 'クイズ結果'
        ordering = ['-completed_at']
        unique_together = [['user', 'quiz', 'completed_at']]

    def __str__(self):
        result = "合格" if self.passed else "不合格"
        return f"{self.user.username} - {self.quiz.title} - {self.score}/{self.total_possible}点 ({self.percentage:.1f}%) [{result}]"
    
    def save(self, *args, **kwargs):
        # 保存前の基本的な処理のみ実行
        # 合格判定
        self.passed = (self.score >= self.quiz.pass_score)
        
        # パーセンテージの計算（設定されていない場合）
        if self.percentage == 0 and self.total_possible > 0:
            self.percentage = (self.score / self.total_possible) * 100
        
        # モデル保存（Supabaseトリガーが統計情報と活動履歴を自動更新）
        super().save(*args, **kwargs) 