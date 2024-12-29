from django.db import models

class MailReceiver(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=100, verbose_name='Ф.И.О')
    comment = models.TextField(verbose_name='Комментарий')

    def __str__(self):
        return f"{self.full_name}: {self.email}"


    class Meta:
        verbose_name = "Получатель рассылки"
        verbose_name_plural = "Получатели рассылки"
        ordering = ["full_name"]


class Message(models.Model):
    title = models.CharField(max_length=100, verbose_name='Тема')
    body = models.TextField(verbose_name='Текст')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"
        ordering = ["title"]


class MailingUnit(models.Model):
    FINISHED = 'Finished'
    CREATED = 'Created'
    LAUNCHED = 'Launched'


    STATUS_CHOICES = [
        (FINISHED, 'Завершена'),
        (CREATED, 'Создана'),
        (LAUNCHED, 'Запущена')
    ]

    started_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата первой отправки")
    finished_at = models.DateTimeField(verbose_name="Дата окончания отправки", blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='message')
    receivers = models.ManyToManyField(MailReceiver, related_name="mailing_units", verbose_name="Получатели")

    def __str__(self):
        return f"{self.receivers}: {self.status}"

    class Meta:
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"
        ordering = ["status", "started_at"]


class MailingAttempt(models.Model):
    SUCCESS = 'Success'
    FAILED = 'Failed'

    STATUS_CHOICES = [
        (SUCCESS, 'Успешно'),
        (FAILED, 'Не успешно')
    ]


    attempt_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата и время попытки')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name='Статус')
    server_answer = models.TextField(verbose_name='Ответ почтового сервера')
    mailing = models.ForeignKey(MailingUnit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.mailing}: {self.status}"

    class Meta:
        verbose_name = "Попытка рассылки"
        verbose_name_plural = "Попытки рассылки"
        ordering = ["mailing", "status", "attempt_at"]
