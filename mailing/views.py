from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View

from .forms import MailingUnitForm, MailReceiverForm, MessageForm
from .models import MailingAttempt, MailingUnit, MailReceiver, Message


class MailingView(View):

    def get(self, request):
        all_mailings = MailingUnit.objects.all().count()
        launched_mailings = MailingUnit.objects.filter(status="Launched").count()
        unique_receivers = MailReceiver.objects.all().count()

        context = {
            "all_mailings": all_mailings,
            "launched_mailings": launched_mailings,
            "unique_receivers": unique_receivers,
        }

        return render(request, "mailing/home.html", context)


class MailReceiverListView(ListView):
    model = MailReceiver
    template_name = "mailing/mail_receiver/mail_receivers_list.html"
    context_object_name = "mail_receivers"


class MailReceiverDetailView(DetailView):
    model = MailReceiver
    template_name = "mailing/mail_receiver/mail_receiver_detail.html"
    context_object_name = "mail_receiver"


class MailReceiverCreateView(CreateView):
    model = MailReceiver
    form_class = MailReceiverForm
    template_name = "mailing/mail_receiver/mail_receiver_form.html"
    context_object_name = "mail_receiver"
    success_url = reverse_lazy("mailing:mail-receivers-list")


class MailReceiverUpdateView(UpdateView):
    model = MailReceiver
    form_class = MailReceiverForm
    context_object_name = "mail_receiver"
    template_name = "mailing/mail_receiver/mail_receiver_form.html"

    def get_success_url(self):
        return reverse_lazy("mailing:mail-receiver-detail", kwargs={"pk": self.object.pk})


class MailReceiverDeleteView(DeleteView):
    model = MailReceiver
    context_object_name = "mail_receiver"
    template_name = "mailing/mail_receiver/mail_receiver_delete.html"
    success_url = reverse_lazy("mailing:home")


class MessageListView(ListView):
    model = Message
    template_name = "mailing/message/messages_list.html"
    context_object_name = "messages"


class MessageDetailView(DetailView):
    model = Message
    template_name = "mailing/message/message_detail.html"
    context_object_name = "message"


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message/message_form.html"
    context_object_name = "message"
    success_url = reverse_lazy("mailing:home")


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message/message_form.html"


    def get_success_url(self):
        return reverse_lazy("mailing:message-detail", kwargs={"pk": self.object.pk})


class MessageDeleteView(DeleteView):
    model = Message
    context_object_name = "message"
    template_name = "mailing/message/message_delete.html"
    success_url = reverse_lazy("mailing:home")


class MailingUnitListView(ListView):
    model = MailingUnit
    template_name = "mailing/mailing_unit/mailing_units_list.html"
    context_object_name = "mailing_units"


class MailingUnitDetailView(DetailView):
    model = MailingUnit
    template_name = "mailing/mailing_unit/mailing_unit_detail.html"
    context_object_name = "mailing_unit"


class MailingUnitCreateView(CreateView):
    model = MailingUnit
    form_class = MailingUnitForm
    template_name = "mailing/mailing_unit/mailing_unit_form.html"
    success_url = reverse_lazy("mailing:mailing-units-list")


class MailingUnitUpdateView(UpdateView):
    model = MailingUnit
    form_class = MailingUnitForm
    template_name = "mailing/mailing_unit/mailing_unit_form.html"
    success_url = reverse_lazy("mailing:mailing-units-list")


class MailingUnitDeleteView(DeleteView):
    model = MailingUnit
    context_object_name = "mailing_unit"
    template_name = "mailing/mailing_unit/mailing_unit_delete.html"
    success_url = reverse_lazy("mailing:mailing-units-list")


class MailingUnitSendMailView(View):
    model = MailingUnit
    context_object_name = "mailing_unit"
    template_name = "mailing/mailing_unit/mailing_unit_detail.html"

    def post(self, request, pk):
        mailing_unit = get_object_or_404(MailingUnit, pk=pk)
        self.send_emails(mailing_unit)
        self.update_status(mailing_unit, "Launched")
        return redirect("mailing:mailing-units-list")

    def send_emails(self, mailing_unit):
        recipients = [receiver.email for receiver in mailing_unit.receivers.all()]
        for receiver in recipients:
            try:
                send_mail(
                    subject=mailing_unit.message.title,
                    message=mailing_unit.message.body,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[receiver],
                    fail_silently=False,
                )
            except BadHeaderError:
                return self.handle_exception("Invalid header found.", receiver, mailing_unit)
            except Exception as e:
                return self.handle_exception(str(e), receiver, mailing_unit)
            else:
                MailingAttempt.objects.create(
                    mailing=mailing_unit, status="Success", server_answer=f"Email успешно отправлен для {receiver}"
                )

    def handle_exception(self, error_message, receiver, mailing_unit):
        MailingAttempt.objects.create(
            mailing=mailing_unit,
            status="Failed",
            server_answer=f'Возникла ошибка: "{error_message}" при отправке на {receiver}',
        )
        return HttpResponse(error_message)

    def update_status(self, mailing_unit, status):
        if mailing_unit.status != status:
            mailing_unit.status = status
            mailing_unit.save()


class MailingUnitStopMailView(View):
    model = MailingUnit
    context_object_name = "mailing_unit"
    template_name = "mailing/mailing_unit/mailing_unit_detail.html"

    def post(self, request, pk):
        mailing_unit = get_object_or_404(MailingUnit, pk=pk)
        mailing_unit.status = "Finished"
        mailing_unit.finished_at = timezone.now()
        mailing_unit.save()
        return redirect("mailing:mailing-units-list")


class MailingAttemptListView(ListView):
    model = MailingAttempt
    template_name = "mailing/mailing_attempts_list.html"
    context_object_name = "mailing_attempts"
    ordering = ["-attempt_at"]

    def get_queryset(self):
        mailing_id = self.kwargs.get("mailing_id")
        return MailingAttempt.objects.filter(mailing=mailing_id).order_by("-attempt_at")

