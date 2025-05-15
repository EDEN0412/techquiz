from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import (
    UserSerializer, 
    UserProfileSerializer, 
    RegisterSerializer, 
    ChangePasswordSerializer
)


class RegisterView(generics.CreateAPIView):
    """ユーザー登録ビュー"""
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ユーザー情報の管理用ビュー"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """現在のユーザーか管理者のみがユーザー情報を取得できます"""
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """現在のログインユーザーの情報を返します"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'], serializer_class=ChangePasswordSerializer)
    def change_password(self, request):
        """パスワード変更機能"""
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            # 新しいパスワードを設定
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'detail': 'パスワードが正常に変更されました'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileViewSet(viewsets.ModelViewSet):
    """ユーザープロファイル管理用ビュー"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """現在のユーザーか管理者のみがプロファイル情報を取得できます"""
        user = self.request.user
        if user.is_staff:
            return UserProfile.objects.all()
        return UserProfile.objects.filter(user=user)


class CustomTokenObtainPairView(TokenObtainPairView):
    """カスタムトークン取得ビュー（必要に応じてカスタマイズ可能）"""
    pass 