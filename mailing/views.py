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


class MailReceiverListViews(ListView):
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
    success_url = reverse_lazy("home")


class MailReceiverUpdateView(UpdateView):
    model = MailReceiver
    template_name = "mailing/mail_receiver/mail_receiver_create.html"
    fields = ["email", "full_name", "comment"]

    def get_success_url(self):
        return reverse_lazy("mail_receiver_detail", kwargs={"pk": self.object.pk})


class MailReceiverDeleteView(DeleteView):
    model = MailReceiver
    context_object_name = "mail_receiver"
    template_name = "mailing/mail_receiver/mail_receiver_delete.html"
    success_url = reverse_lazy("home")

