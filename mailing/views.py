from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View

from .forms import MailingUnitForm, MailReceiverForm, MessageForm
from .models import MailingAttempt, MailingUnit, MailReceiver, Message


class MailingView(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.has_perm("view_mailingunit"):
            all_mailings = MailingUnit.objects.all().count()
            launched_mailings = MailingUnit.objects.filter(status="Launched").count()
            unique_receivers = MailReceiver.objects.all().count()
        else:
            all_mailings = MailingUnit.objects.filter(owner_id=request.user.id).count()
            launched_mailings = MailingUnit.objects.filter(status="Launched", owner_id=request.user.id).count()
            unique_receivers = MailReceiver.objects.filter(owner_id=request.user.id).count()

        context = {
            "all_mailings": all_mailings,
            "launched_mailings": launched_mailings,
            "unique_receivers": unique_receivers,
        }

        return render(request, "mailing/home.html", context)


class MailReceiverListView(LoginRequiredMixin, ListView):
    model = MailReceiver
    template_name = "mailing/mail_receiver/mail_receivers_list.html"
    context_object_name = "mail_receivers"

    def get_queryset(self):
        if self.request.user.has_perm("view_mailreceiver"):
            return MailReceiver.objects.all()
        return MailReceiver.objects.filter(owner=self.request.user)


class MailReceiverDetailView(LoginRequiredMixin, DetailView):
    model = MailReceiver
    template_name = "mailing/mail_receiver/mail_receiver_detail.html"
    context_object_name = "mail_receiver"


class MailReceiverCreateView(LoginRequiredMixin, CreateView):
    model = MailReceiver
    form_class = MailReceiverForm
    template_name = "mailing/mail_receiver/mail_receiver_form.html"
    context_object_name = "mail_receiver"
    success_url = reverse_lazy("mailing:mail-receivers-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailReceiverUpdateView(LoginRequiredMixin, UpdateView):
    model = MailReceiver
    form_class = MailReceiverForm
    context_object_name = "mail_receiver"
    template_name = "mailing/mail_receiver/mail_receiver_form.html"

    def get_success_url(self):
        return reverse_lazy("mailing:mail-receiver-detail", kwargs={"pk": self.object.pk})


class MailReceiverDeleteView(LoginRequiredMixin, DeleteView):
    model = MailReceiver
    context_object_name = "mail_receiver"
    template_name = "mailing/mail_receiver/mail_receiver_delete.html"
    success_url = reverse_lazy("mailing:home")


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailing/message/messages_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        return Message.objects.filter(owner=self.request.user)


class MessageDetailView(LoginRequiredMixin, DetailView):
    model = Message
    template_name = "mailing/message/message_detail.html"
    context_object_name = "message"


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message/message_form.html"
    context_object_name = "message"
    success_url = reverse_lazy("mailing:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    template_name = "mailing/message/message_form.html"

    def get_success_url(self):
        return reverse_lazy("mailing:message-detail", kwargs={"pk": self.object.pk})


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    context_object_name = "message"
    template_name = "mailing/message/message_delete.html"
    success_url = reverse_lazy("mailing:home")


class MailingUnitListView(LoginRequiredMixin, ListView):
    model = MailingUnit
    template_name = "mailing/mailing_unit/mailing_units_list.html"
    context_object_name = "mailing_units"

    def get_queryset(self):
        if self.request.user.has_perm("view_mailingunit"):
            return MailingUnit.objects.all()
        return MailingUnit.objects.filter(owner=self.request.user)


class MailingUnitDetailView(LoginRequiredMixin, DetailView):
    model = MailingUnit
    template_name = "mailing/mailing_unit/mailing_unit_detail.html"
    context_object_name = "mailing_unit"


class MailingUnitCreateView(LoginRequiredMixin, CreateView):
    model = MailingUnit
    form_class = MailingUnitForm
    template_name = "mailing/mailing_unit/mailing_unit_form.html"
    success_url = reverse_lazy("mailing:mailing-units-list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingUnitUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingUnit
    form_class = MailingUnitForm
    template_name = "mailing/mailing_unit/mailing_unit_form.html"
    success_url = reverse_lazy("mailing:mailing-units-list")


class MailingUnitDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingUnit
    context_object_name = "mailing_unit"
    template_name = "mailing/mailing_unit/mailing_unit_delete.html"
    success_url = reverse_lazy("mailing:mailing-units-list")


class MailingUnitSendMailView(LoginRequiredMixin, View):
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


class MailingUnitStopMailView(LoginRequiredMixin, View):
    model = MailingUnit
    context_object_name = "mailing_unit"
    template_name = "mailing/mailing_unit/mailing_unit_detail.html"

    def post(self, request, pk):
        mailing_unit = get_object_or_404(MailingUnit, pk=pk)
        mailing_unit.status = "Finished"
        mailing_unit.finished_at = timezone.now()
        mailing_unit.save()
        return redirect("mailing:mailing-units-list")


class MailingAttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = "mailing/mailing_attempts_list.html"
    context_object_name = "mailing_attempts"
    ordering = ["-attempt_at"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.get_queryset().exists():
            context["message"] = self.get_queryset().first().mailing.message
        return context

    def get_queryset(self):
        mailing_id = self.kwargs.get("mailing_id")
        if mailing_id:
            return MailingAttempt.objects.filter(mailing=mailing_id).order_by("-attempt_at")
        return MailingAttempt.objects.filter(mailing__owner=self.request.user).order_by("-attempt_at")
