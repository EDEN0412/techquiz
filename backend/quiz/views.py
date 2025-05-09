"""
クイズアプリのビュー定義
"""

from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Avg, Count, Sum
from django.shortcuts import get_object_or_404

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
from .serializers import (
    CategorySerializer,
    DifficultyLevelSerializer,
    QuizSerializer,
    QuizDetailSerializer,
    QuestionSerializer,
    AnswerSerializer,
    QuizResultSerializer,
    UserStatisticsSerializer,
    ActivityHistorySerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    カテゴリのCRUD操作のためのエンドポイント
    
    list:
        すべてのカテゴリを取得する
    retrieve:
        特定のカテゴリを取得する
    create:
        新しいカテゴリを作成する
    update:
        カテゴリを更新する
    partial_update:
        カテゴリを部分的に更新する
    destroy:
        カテゴリを削除する
    """
    queryset = Category.objects.all().order_by('display_order')
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'description']
    filterset_fields = ['is_active']
    ordering_fields = ['name', 'display_order', 'created_at']
    
    @action(detail=True, methods=['get'])
    def quizzes(self, request, pk=None):
        """
        特定のカテゴリに属するクイズのリストを取得する
        """
        category = self.get_object()
        quizzes = Quiz.objects.filter(category=category, is_active=True)
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)


class DifficultyLevelViewSet(viewsets.ModelViewSet):
    """
    難易度レベルのCRUD操作のためのエンドポイント
    """
    queryset = DifficultyLevel.objects.all().order_by('level')
    serializer_class = DifficultyLevelSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['level', 'name', 'created_at']
    
    @action(detail=True, methods=['get'])
    def quizzes(self, request, pk=None):
        """
        特定の難易度に属するクイズのリストを取得する
        """
        difficulty = self.get_object()
        quizzes = Quiz.objects.filter(difficulty=difficulty, is_active=True)
        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data)


class QuizViewSet(viewsets.ModelViewSet):
    """
    クイズのCRUD操作のためのエンドポイント
    """
    queryset = Quiz.objects.all()
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['title', 'description']
    filterset_fields = ['category', 'difficulty', 'is_active']
    ordering_fields = ['title', 'created_at', 'category', 'difficulty']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return QuizDetailSerializer
        return QuizSerializer
    
    @action(detail=True, methods=['get'])
    def questions(self, request, pk=None):
        """
        特定のクイズに属する問題のリストを取得する
        """
        quiz = self.get_object()
        questions = Question.objects.filter(quiz=quiz).order_by('display_order')
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)


class QuestionViewSet(viewsets.ModelViewSet):
    """
    問題のCRUD操作のためのエンドポイント
    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend, filters.OrderingFilter]
    search_fields = ['question_text']
    filterset_fields = ['quiz', 'question_type']
    ordering_fields = ['display_order', 'created_at']
    
    @action(detail=True, methods=['get'])
    def answers(self, request, pk=None):
        """
        特定の問題に属する回答のリストを取得する
        """
        question = self.get_object()
        answers = Answer.objects.filter(question=question).order_by('display_order')
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)


class AnswerViewSet(viewsets.ModelViewSet):
    """
    回答のCRUD操作のためのエンドポイント
    """
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['question', 'is_correct']
    ordering_fields = ['display_order', 'created_at']


class QuizResultViewSet(viewsets.ModelViewSet):
    """
    クイズ結果のCRUD操作のためのエンドポイント
    """
    queryset = QuizResult.objects.all()
    serializer_class = QuizResultSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'quiz', 'passed']
    ordering_fields = ['score', 'percentage', 'completed_at', 'created_at']
    
    def get_queryset(self):
        """
        現在のユーザーのクイズ結果のみを返す、もしくは管理者の場合は全てのクイズ結果を返す
        """
        user = self.request.user
        if user.is_staff:
            return QuizResult.objects.all()
        return QuizResult.objects.filter(user=user)
    
    def perform_create(self, serializer):
        """
        クイズ結果を保存する際に、ユーザーとpassedフラグを自動的に設定する
        """
        quiz = serializer.validated_data.get('quiz')
        score = serializer.validated_data.get('score')
        total_possible = serializer.validated_data.get('total_possible', 0)
        
        # パスしたかどうかを計算
        passed = False
        if total_possible > 0:
            percentage = (score / total_possible) * 100
            passed = percentage >= quiz.pass_score
        
        serializer.save(user=self.request.user, passed=passed)


class UserStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ユーザー統計情報の取得のためのエンドポイント（読み取り専用）
    """
    serializer_class = UserStatisticsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'category', 'difficulty']
    ordering_fields = ['quizzes_completed', 'total_points', 'avg_score', 'highest_score', 'last_quiz_date']
    
    def get_queryset(self):
        """
        現在のユーザーの統計情報のみを返す、もしくは管理者の場合は全てのユーザーの統計情報を返す
        """
        user = self.request.user
        if user.is_staff:
            return UserStatistics.objects.all()
        return UserStatistics.objects.filter(user=user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """
        ユーザーの全体的な統計情報のサマリーを取得する
        """
        user = request.user
        stats = UserStatistics.objects.filter(user=user)
        
        # 全体の統計情報を計算
        total_quizzes = stats.aggregate(total=Sum('quizzes_completed'))['total'] or 0
        total_points = stats.aggregate(total=Sum('total_points'))['total'] or 0
        avg_score = stats.aggregate(avg=Avg('avg_score'))['avg'] or 0
        
        # カテゴリごとの統計
        categories = UserStatistics.objects.filter(
            user=user, 
            difficulty=None
        ).order_by('-quizzes_completed')
        
        # 難易度ごとの統計
        difficulties = UserStatistics.objects.filter(
            user=user, 
            category=None
        ).order_by('-quizzes_completed')
        
        # 結果をシリアライズ
        category_serializer = UserStatisticsSerializer(categories, many=True)
        difficulty_serializer = UserStatisticsSerializer(difficulties, many=True)
        
        return Response({
            'total_quizzes_completed': total_quizzes,
            'total_points': total_points,
            'overall_avg_score': avg_score,
            'categories': category_serializer.data,
            'difficulties': difficulty_serializer.data
        })


class ActivityHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    活動履歴の取得のためのエンドポイント（読み取り専用）
    """
    serializer_class = ActivityHistorySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'quiz', 'category', 'difficulty', 'activity_type']
    ordering_fields = ['activity_date', 'score', 'percentage']
    
    def get_queryset(self):
        """
        現在のユーザーの活動履歴のみを返す、もしくは管理者の場合は全てのユーザーの活動履歴を返す
        """
        user = self.request.user
        if user.is_staff:
            return ActivityHistory.objects.all().order_by('-activity_date')
        return ActivityHistory.objects.filter(user=user).order_by('-activity_date')
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        ユーザーの最近の活動履歴を取得する
        """
        user = request.user
        limit = int(request.query_params.get('limit', 10))
        activities = ActivityHistory.objects.filter(user=user).order_by('-activity_date')[:limit]
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)
