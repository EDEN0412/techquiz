# Generated by Django 5.1.7 on 2025-04-25 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quiz", "0005_testsupabasemodel"),
    ]

    operations = [
        migrations.AddField(
            model_name="testsupabasemodel",
            name="test_field",
            field=models.CharField(
                blank=True, max_length=50, null=True, verbose_name="テストフィールド"
            ),
        ),
    ]
