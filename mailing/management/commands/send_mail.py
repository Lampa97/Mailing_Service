from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.core.management.base import BaseCommand

from mailing.models import MailingAttempt, MailingUnit, Message


class Command(BaseCommand):
    help = """This command sends emails to all receivers in the mailing. It takes the title of the message as an argument.
    Example: python manage.py send_mail "Title of the message" """

    def add_arguments(self, parser):
        parser.add_argument("title", type=str, help="Title of the message to send")

    def handle(self, *args, **kwargs):
        title = kwargs["title"]
        message = Message.objects.get(title=title)
        mailing = MailingUnit.objects.get(message_id=message.id)
        self.__send_emails(mailing)
        self.__update_status(mailing, "Launched")

        self.stdout.write(self.style.SUCCESS("Mailing was launched successfully"))

    def __send_emails(self, mailing_unit):
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
                return self.__handle_exception("Invalid header found.", receiver, mailing_unit)
            except Exception as e:
                return self.__handle_exception(str(e), receiver, mailing_unit)
            else:
                MailingAttempt.objects.create(
                    mailing=mailing_unit, status="Success", server_answer=f"Email успешно отправлен для {receiver}"
                )

    def __handle_exception(self, error_message, receiver, mailing_unit):
        MailingAttempt.objects.create(
            mailing=mailing_unit,
            status="Failed",
            server_answer=f'Возникла ошибка: "{error_message}" при отправке на {receiver}',
        )

    def __update_status(self, mailing_unit, status):
        if mailing_unit.status != status:
            mailing_unit.status = status
            mailing_unit.save()
