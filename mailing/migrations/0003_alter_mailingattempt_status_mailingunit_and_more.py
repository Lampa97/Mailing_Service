# Generated by Django 5.1.4 on 2024-12-29 02:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0002_alter_mailing_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailingattempt",
            name="status",
            field=models.CharField(
                choices=[("Success", "Успешно"), ("Failed", "Не успешно")], max_length=10, verbose_name="Статус"
            ),
        ),
        migrations.CreateModel(
            name="MailingUnit",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("started_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата первой отправки")),
                ("finished_at", models.DateTimeField(blank=True, verbose_name="Дата окончания отправки")),
                (
                    "status",
                    models.CharField(
                        choices=[("Finished", "Завершена"), ("Created", "Создана"), ("Launched", "Запущена")],
                        max_length=10,
                        verbose_name="Статус",
                    ),
                ),
                (
                    "message",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name="message", to="mailing.message"
                    ),
                ),
                ("receivers", models.ManyToManyField(to="mailing.mailreceiver")),
            ],
            options={
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
                "ordering": ["status", "started_at"],
            },
        ),
        migrations.AlterField(
            model_name="mailingattempt",
            name="mailing",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="mailing.mailingunit"),
        ),
        migrations.DeleteModel(
            name="Mailing",
        ),
    ]
