# Generated by Django 5.1.5 on 2025-01-30 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0008_remove_customuser_password_change_token"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="password_reset_token",
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name="Token"),
        ),
    ]
