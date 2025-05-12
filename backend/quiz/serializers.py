"""
クイズアプリのシリアライザー定義
"""

from rest_framework import serializers
from .models import (
    Category, 
    DifficultyLevel,
    Quiz,
    Question,
    Answer,
    QuizResult,
    UserStatistics,
    ActivityHistory
)


class CategorySerializer(serializers.ModelSerializer):
    """カテゴリーシリアライザー"""
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'icon', 
            'display_order', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class DifficultyLevelSerializer(serializers.ModelSerializer):
    """難易度シリアライザー"""
    
    class Meta:
        model = DifficultyLevel
        fields = [
            'id', 'name', 'slug', 'level', 'description', 
            'point_multiplier', 'time_limit', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AnswerSerializer(serializers.ModelSerializer):
    """回答シリアライザー"""
    
    class Meta:
        model = Answer
        fields = [
            'id', 'question', 'answer_text', 'is_correct', 
            'feedback', 'display_order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class QuestionSerializer(serializers.ModelSerializer):
    """問題シリアライザー"""
    
    answers = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = [
            'id', 'quiz', 'question_text', 'question_type', 
            'hint', 'explanation', 'points', 'display_order', 
            'code_snippet', 'image_url', 'media_type', 
            'syntax_highlight', 'answers', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class QuizSerializer(serializers.ModelSerializer):
    """クイズシリアライザー"""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    difficulty_name = serializers.CharField(source='difficulty.name', read_only=True)
    
    class Meta:
        model = Quiz
        fields = [
            'id', 'category', 'category_name', 'difficulty', 'difficulty_name',
            'title', 'description', 'time_limit', 'pass_score', 'is_active',
            'thumbnail_url', 'banner_image_url', 'media_type', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class QuizDetailSerializer(QuizSerializer):
    """クイズ詳細シリアライザー（問題を含む）"""
    
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta(QuizSerializer.Meta):
        fields = QuizSerializer.Meta.fields + ['questions']


class QuizResultSerializer(serializers.ModelSerializer):
    """クイズ結果シリアライザー"""
    
    username = serializers.CharField(source='user.username', read_only=True)
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    category_name = serializers.CharField(source='quiz.category.name', read_only=True)
    difficulty_name = serializers.CharField(source='quiz.difficulty.name', read_only=True)
    
    class Meta:
        model = QuizResult
        fields = [
            'id', 'user', 'username', 'quiz', 'quiz_title', 
            'category_name', 'difficulty_name', 
            'score', 'total_possible', 'percentage', 
            'time_taken', 'passed', 'completed_at', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'passed']


class UserStatisticsSerializer(serializers.ModelSerializer):
    """ユーザー統計情報シリアライザー"""
    
    username = serializers.CharField(source='user.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    difficulty_name = serializers.SerializerMethodField()
    
    class Meta:
        model = UserStatistics
        fields = [
            'id', 'user', 'username', 'category', 'category_name', 
            'difficulty', 'difficulty_name', 'quizzes_completed', 
            'total_points', 'avg_score', 'highest_score', 
            'last_quiz_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_difficulty_name(self, obj):
        """難易度名を取得（難易度がNoneの場合は「全難易度」を返す）"""
        return obj.difficulty.name if obj.difficulty else "全難易度"


class ActivityHistorySerializer(serializers.ModelSerializer):
    """活動履歴シリアライザー"""
    
    username = serializers.CharField(source='user.username', read_only=True)
    quiz_title = serializers.CharField(source='quiz.title', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    difficulty_name = serializers.CharField(source='difficulty.name', read_only=True)
    activity_type_display = serializers.CharField(source='get_activity_type_display', read_only=True)
    
    class Meta:
        model = ActivityHistory
        fields = [
            'id', 'user', 'username', 'quiz', 'quiz_title', 
            'category', 'category_name', 'difficulty', 'difficulty_name', 
            'score', 'percentage', 'activity_date', 
            'activity_type', 'activity_type_display',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at'] 