from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from techskillsquiz.supabase_sync.models import SupabaseModelMixin


class UserProfile(SupabaseModelMixin, models.Model):
    """ユーザープロファイルモデル。標準ユーザーモデルを拡張します。"""
    
    supabase_table = 'user_profile'
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    avatar_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """ユーザーが作成されたときに自動的にプロファイルを作成します。"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """ユーザーが保存されたときにプロファイルも保存します。"""
    instance.profile.save() 