# Generated by Django 5.1.5 on 2025-01-27 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_alter_customuser_avatar"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="avatar",
            field=models.ImageField(
                blank=True,
                default="avatars/default_avatar.jpg",
                null=True,
                upload_to="avatars/",
                verbose_name="Avatar",
            ),
        ),
    ]
