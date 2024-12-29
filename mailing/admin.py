from django.contrib import admin

from .models import MailReceiver, MailingUnit, MailingAttempt, Message

@admin.register(MailReceiver)
class MailReceiverAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name")
    search_fields = ("email", "full_name", "comment")


@admin.register(MailingUnit)
class MailingUnitAdmin(admin.ModelAdmin):
    list_display = ("status", "started_at", "finished_at")
    list_filter = ["status"]
    search_fields = ("status", "receivers")


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("status", "get_receivers", "attempt_at")
    list_filter = ["attempt_at", "status"]
    search_fields = ("status",)

    @admin.display(description="Получатели")
    def get_receivers(self, obj):
        return [f"{receiver.full_name}: {receiver.email}" for receiver in obj.mailing.receivers.all()]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("title",)
    search_fields = ("title",)
