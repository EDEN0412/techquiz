# Generated by Django 5.1.7 on 2025-04-15 04:28

import techskillsquiz.supabase_mixins
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0004_auto_20250414_1535"),
    ]

    operations = [
        migrations.CreateModel(
            name="TestSupabaseModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="名前")),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="説明"),
                ),
                ("is_active", models.BooleanField(default=True, verbose_name="有効")),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, verbose_name="作成日時"),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="更新日時"),
                ),
            ],
            options={
                "verbose_name": "テストモデル",
                "verbose_name_plural": "テストモデル",
            },
            bases=(models.Model, techskillsquiz.supabase_mixins.SupabaseModelMixin),
        ),
    ]
