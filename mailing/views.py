from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View
from django.core.mail import send_mail
from django.conf import settings
from .forms import MailingUnitForm
from django.utils import timezone
from .models import MailingUnit, MailReceiver, Message


class MailingView(TemplateView):

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
    template_name = "mailing/mail_receiver/mail_receiver_create.html"
    context_object_name = "mail_receiver"
    fields = ["email", "full_name", "comment"]
    success_url = reverse_lazy("mailing:home")


class MailReceiverUpdateView(UpdateView):
    model = MailReceiver
    template_name = "mailing/mail_receiver/mail_receiver_update.html"
    fields = ["email", "full_name", "comment"]

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
    template_name = "mailing/message/message_create.html"
    context_object_name = "message"
    fields = [
        "title",
        "body",
    ]
    success_url = reverse_lazy("mailing:home")


class MessageUpdateView(UpdateView):
    model = Message
    template_name = "mailing/message/message_update.html"
    fields = [
        "title",
        "body",
    ]

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
        send_mail(
            subject=mailing_unit.message.title,
            message=mailing_unit.message.body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[receiver.email for receiver in mailing_unit.receivers.all()],
        )
        # Update status to 'Launched'
        if mailing_unit.status != 'Launched':
            mailing_unit.status = 'Launched'
            mailing_unit.save()
        return redirect('mailing:mailing-units-list')

class MailingUnitStopMailView(View):
    model = MailingUnit
    context_object_name = "mailing_unit"
    template_name = "mailing/mailing_unit/mailing_unit_detail.html"

    def post(self, request, pk):
        mailing_unit = get_object_or_404(MailingUnit, pk=pk)
        mailing_unit.status = 'Finished'
        mailing_unit.finished_at = timezone.now()
        mailing_unit.save()
        return redirect('mailing:mailing-units-list')