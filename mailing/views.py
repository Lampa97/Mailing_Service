from django.shortcuts import render

from django.urls import reverse_lazy

from .models import MailingUnit, MailReceiver, MailingAttempt, Message

from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView, ListView


class MailingView(TemplateView):

    def get(self, request):
        all_mailings = MailingUnit.objects.all().count()
        launched_mailings = MailingUnit.objects.filter(status='Launched').count()
        unique_receivers = MailReceiver.objects.all().count()

        context = {"all_mailings": all_mailings, "launched_mailings": launched_mailings, "unique_receivers": unique_receivers}

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
    fields = ["title", "body",]
    success_url = reverse_lazy("mailing:home")


class MessageUpdateView(UpdateView):
    model = Message
    template_name = "mailing/message/message_update.html"
    fields = ["title", "body",]

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
    template_name = "mailing/mailing_unit/mailing_unit_create.html"
    context_object_name = "mailing_unit"
    fields = ["message", "receivers",]
    success_url = reverse_lazy("mailing:home")

    def form_valid(self, form):
        if len(form.instance.receivers) < 1:
            form.instance.status = "Created"
        else:
            form.instance.status = "Launched"
        return super().form_valid(form)

class MailingUnitUpdateView(UpdateView):
    model = MailingUnit
    template_name = "mailing/mailing_unit/mailing_unit_update.html"
    fields = ["message", "receivers",]

    def get_success_url(self):
        return reverse_lazy("mailing:mailing-unit-detail", kwargs={"pk": self.object.pk})


class MailingUnitDeleteView(DeleteView):
    model = MailingUnit
    context_object_name = "mailing_unit"
    template_name = "mailing/mailing_unit/mailing_unit_delete.html"
    success_url = reverse_lazy("mailing:home")