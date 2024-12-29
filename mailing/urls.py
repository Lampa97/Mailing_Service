from django.urls import path

from . import views

app_name = "mailing"

urlpatterns = [
    path("", views.MailingView.as_view(), name="home"),
    path("mail-receivers-list", views.MailReceiverListViews.as_view(), name="mail-receivers-list"),
    path("mail-receiver-detail/", views.MailReceiverDetailView.as_view(), name="mail-receiver-detail"),
    path("mail-receiver-create/", views.MailReceiverCreateView.as_view(), name="mail-receiver-create"),
    path("mail-receiver-update/", views.MailReceiverUpdateView.as_view(), name="mail-receiver-update"),
    path("mail-receiver-delete/", views.MailReceiverDeleteView.as_view(), name="mail-receiver-delete")
]