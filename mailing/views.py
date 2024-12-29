from django.shortcuts import render

from django.urls import reverse_lazy

from .models import Mailing, MailReceiver, MailingAttempt, Message

from django.views.generic import TemplateView, CreateView, DetailView, UpdateView, DeleteView

ALL_MAILINGS = Mailing.objects.all()
UNIQUE_RECEIVERS = MailReceiver.objects.all()

class MailingView(TemplateView):
    model = Mailing
    context_object_name = "mailing"
    template_name = "mailing/home.html"

    def get(self, request):
        all_mailings = ALL_MAILINGS.count()
        launched_mailings = Mailing.objects.filter(status='Launched').count()
        unique_receivers = UNIQUE_RECEIVERS.count()

        context = {"all_mailings": all_mailings, "launched_mailings": launched_mailings, "unique_receivers": unique_receivers}

        print(all_mailings)
        return render(request, "mailing/home.html", context)


