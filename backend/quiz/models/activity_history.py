"""
ユーザー活動履歴モデル
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from techskillsquiz.supabase_mixins import SupabaseModelMixin
from .quiz import Quiz
from .category import Category
from .difficulty import DifficultyLevel

User = get_user_model()


class ActivityHistory(models.Model, SupabaseModelMixin):
    """
    ユーザー活動履歴モデル - ユーザーのクイズ活動履歴を記録
    """
    supabase_table = 'quiz_activityhistory'

    ACTIVITY_TYPES = (
        ('quiz_completed', 'クイズ完了'),
        ('quiz_started', 'クイズ開始'),
        ('quiz_review', 'クイズ復習'),
        ('achievement_earned', '実績獲得'),
    )

    user = models.ForeignKey(
        User, 
        verbose_name='ユーザー',
        on_delete=models.CASCADE, 
        related_name='activity_history'
    )
    quiz = models.ForeignKey(
        Quiz, 
        verbose_name='クイズ',
        on_delete=models.CASCADE, 
        related_name='activity_history'
    )
    category = models.ForeignKey(
        Category, 
        verbose_name='カテゴリ',
        on_delete=models.SET_NULL, 
        related_name='activity_history',
        null=True
    )
    difficulty = models.ForeignKey(
        DifficultyLevel, 
        verbose_name='難易度',
        on_delete=models.SET_NULL, 
        related_name='activity_history',
        null=True
    )
    score = models.PositiveIntegerField('スコア', default=0)
    percentage = models.FloatField('正答率', default=0.0)
    activity_date = models.DateTimeField('活動日時', auto_now_add=True)
    activity_type = models.CharField(
        '活動タイプ', 
        max_length=20, 
        choices=ACTIVITY_TYPES, 
        default='quiz_completed'
    )
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時', auto_now=True)

    class Meta:
        verbose_name = '活動履歴'
        verbose_name_plural = '活動履歴'
        ordering = ['-activity_date']
        indexes = [
            models.Index(fields=['user', '-activity_date']),
            models.Index(fields=['user', 'category']),
            models.Index(fields=['user', 'activity_type']),
        ]

    def __str__(self):
        activity = dict(self.ACTIVITY_TYPES).get(self.activity_type, self.activity_type)
        return f"{self.user.username} - {activity} - {self.quiz.title} - {self.score}点 ({self.percentage:.1f}%)"
    
    def save(self, *args, **kwargs):
        # カテゴリと難易度が設定されていない場合、クイズから設定
        if self.quiz and not self.category:
            self.category = self.quiz.category
            
        if self.quiz and not self.difficulty:
            self.difficulty = self.quiz.difficulty
            
        # Djangoモデルを保存（post_saveシグナルがSupabase同期を担当）
        super().save(*args, **kwargs)
        
        # 古い履歴データのアーカイブをチェック（新規作成時のみ、かつ10％の確率で実行）
        if not self.id and __import__('random').random() < 0.1:
            self._check_old_activities()
    
    @classmethod
    def create_from_quiz_result(cls, quiz_result, activity_type='quiz_completed'):
        """
        クイズ結果から活動履歴を作成するファクトリメソッド
        
        Args:
            quiz_result: QuizResultインスタンス
            activity_type: 活動タイプ
            
        Returns:
            作成された活動履歴
        """
        return cls.objects.create(
            user=quiz_result.user,
            quiz=quiz_result.quiz,
            category=quiz_result.quiz.category,
            difficulty=quiz_result.quiz.difficulty,
            score=quiz_result.score,
            percentage=quiz_result.percentage,
            activity_type=activity_type
        )
    
    def _check_old_activities(self):
        """
        古い活動履歴をアーカイブまたは削除
        
        注: パフォーマンスへの影響を考慮し、一定確率でのみ実行
        
        ※現在は古い活動履歴の削除が無効化されています。
        """
        # 設定から保持期間を取得（デフォルト90日）
        from django.conf import settings
        retention_days = getattr(settings, 'ACTIVITY_HISTORY_RETENTION_DAYS', 90)
        
        # 削除基準日を計算
        cutoff_date = timezone.now() - timedelta(days=retention_days)
        
        try:
            # 古い活動履歴の数を確認するだけで、削除は行わない
            old_activities_count = ActivityHistory.objects.filter(
                user=self.user,
                activity_date__lt=cutoff_date
            ).count()
            
            if old_activities_count > 0:
                import logging
                logger = logging.getLogger(__name__)
                logger.info(f"ユーザー {self.user.username} の古い活動履歴が {old_activities_count}件 存在しますが、削除は無効化されています")
            
            # 以下の削除処理は無効化されています
            # old_activities = ActivityHistory.objects.filter(
            #     user=self.user,
            #     activity_date__lt=cutoff_date
            # ).order_by('activity_date')[:10]
            
            # # 削除を実行（本番環境では、アーカイブテーブルへの移動などの処理が適切）
            # count = 0
            # for activity in old_activities:
            #     activity.delete()  # これによりSupabaseからも削除される
            #     count += 1
                
            # if count > 0:
            #     import logging
            #     logger = logging.getLogger(__name__)
            #     logger.info(f"ユーザー {self.user.username} の古い活動履歴 {count}件 をクリーンアップしました")
                
        except Exception as e:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"活動履歴のクリーンアップ確認中にエラー: {str(e)}") 