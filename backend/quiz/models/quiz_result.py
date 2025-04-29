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
        # 保存前に合格判定
        is_new = not self.id  # 新規作成かどうかの判定
        
        if is_new:  # 新規作成時のみ
            self.passed = (self.score >= self.quiz.pass_score)
            if self.percentage == 0 and self.total_possible > 0:
                self.percentage = (self.score / self.total_possible) * 100
        
        # Djangoモデルを保存（post_saveシグナルがSupabase同期を担当）
        super().save(*args, **kwargs)
        
        # 新規作成時のみ、関連する統計情報と活動履歴を更新
        if is_new:
            # 統計情報の更新
            self._update_user_statistics()
            
            # 活動履歴の作成
            self._create_activity_history()
    
    def _update_user_statistics(self):
        """
        ユーザー統計情報を更新
        """
        try:
            # ここではUserStatisticsモデルを直接インポートせず、循環インポートを防止
            from .user_statistics import UserStatistics
            
            # 統計情報の更新（既に存在すれば取得、なければ作成）
            stats, created = UserStatistics.objects.get_or_create(
                user=self.user,
                category=self.quiz.category,
                defaults={
                    'completed_quizzes': 1,
                    'total_score': self.score,
                    'total_possible': self.total_possible,
                    'total_time': self.time_taken,
                    'passed_quizzes': 1 if self.passed else 0,
                }
            )
            
            # 既存の統計を更新
            if not created:
                stats.completed_quizzes += 1
                stats.total_score += self.score
                stats.total_possible += self.total_possible
                stats.total_time += self.time_taken
                if self.passed:
                    stats.passed_quizzes += 1
                stats.save()  # 統計情報を保存（これによりSupabase同期も行われる）
        
        except Exception as e:
            # エラーログを出力するが、このエラーでクイズ結果の保存自体を失敗させない
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"クイズ結果保存後の統計更新中にエラー: {str(e)}")
    
    def _create_activity_history(self):
        """
        活動履歴を作成
        """
        try:
            # ここではActivityHistoryモデルを直接インポートせず、循環インポートを防止
            from .activity_history import ActivityHistory
            
            # 活動履歴を作成
            ActivityHistory.create_from_quiz_result(self)
        
        except Exception as e:
            # エラーログを出力するが、このエラーでクイズ結果の保存自体を失敗させない
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"クイズ結果保存後の活動履歴作成中にエラー: {str(e)}") 