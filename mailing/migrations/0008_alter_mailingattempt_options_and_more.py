# Generated by Django 5.1.4 on 2025-01-02 10:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("mailing", "0007_alter_mailingunit_message_alter_mailingunit_status"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="mailingattempt",
            options={
                "ordering": ["-attempt_at", "mailing", "status"],
                "verbose_name": "Попытка рассылки",
                "verbose_name_plural": "Попытки рассылки",
            },
        ),
        migrations.AlterModelOptions(
            name="mailingunit",
            options={
                "ordering": ["-status", "started_at"],
                "verbose_name": "Рассылка",
                "verbose_name_plural": "Рассылки",
            },
        ),
        migrations.AlterModelOptions(
            name="mailreceiver",
            options={
                "ordering": ["email"],
                "verbose_name": "Получатель рассылки",
                "verbose_name_plural": "Получатели рассылки",
            },
        ),
    ]
