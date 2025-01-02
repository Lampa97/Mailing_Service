import logging
from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.core.mail import send_mail
from django.conf import settings
from mailing.models import MailingUnit, MailingAttempt

logger = logging.getLogger(__name__)

def send_emails():
    mailing_units = MailingUnit.objects.filter(status__in=['Created', 'Launched'])
    for mailing_unit in mailing_units:
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
                MailingAttempt.objects.create(
                    mailing=mailing_unit, status="Success", server_answer=f"Email успешно отправлен для {receiver}"
                )
            except Exception as e:
                MailingAttempt.objects.create(
                    mailing=mailing_unit, status="Failed", server_answer=f'Возникла ошибка: "{str(e)}" при отправке на {receiver}'
                )
        mailing_unit.status = 'Launched'
        mailing_unit.save()

class Command(BaseCommand):
    help = "Starts the APScheduler to send emails"

    def handle(self, *args, **kwargs):
        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        # Schedule the job to run every day at 8:00 AM
        scheduler.add_job(
            send_emails,
            trigger=CronTrigger(hour="11", minute="0"),
            id="send_emails",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_emails'.")

        register_events(scheduler)
        scheduler.start()
        logger.info("Scheduler started.")

        self.stdout.write(self.style.SUCCESS("Scheduler started successfully"))