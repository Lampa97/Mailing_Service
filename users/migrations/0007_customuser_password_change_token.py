# Generated by Django 5.1.5 on 2025-01-30 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0006_customuser_token"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="password_change_token",
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name="Password_Change_Token"),
        ),
    ]
