from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    """ユーザープロファイル用シリアライザー"""
    
    class Meta:
        model = UserProfile
        fields = ('bio', 'date_of_birth', 'avatar_url', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')


class UserSerializer(serializers.ModelSerializer):
    """ユーザー情報用シリアライザー"""
    
    profile = UserProfileSerializer(required=False)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'profile', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class RegisterSerializer(serializers.ModelSerializer):
    """ユーザー登録用シリアライザー"""
    
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True, 
        required=True, 
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }
    
    def validate(self, attrs):
        """パスワードの一致を検証します"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'パスワードが一致しません'})
        return attrs
    
    def create(self, validated_data):
        """ユーザーを作成し、パスワードをハッシュ化します"""
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        
        user.set_password(validated_data['password'])
        user.save()
        
        return user


class ChangePasswordSerializer(serializers.Serializer):
    """パスワード変更用シリアライザー"""
    
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    
    def validate_old_password(self, value):
        """古いパスワードが正しいか検証します"""
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('古いパスワードが正しくありません')
        return value 