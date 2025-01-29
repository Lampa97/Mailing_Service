from django.core.cache import cache

from config.settings import CACHE_ENABLED
from .models import MailingUnit, Message, MailReceiver, MailingAttempt

CACHE_TIMEOUT = 60

class MailingUnitService:

    @staticmethod
    def get_all_mailing_units():
        if not CACHE_ENABLED:
            return MailingUnit.objects.all()
        key = "mailing_units"
        mailing_units = cache.get(key)
        if mailing_units is not None:
            return mailing_units
        mailing_units = MailingUnit.objects.all()
        cache.set(key, mailing_units, CACHE_TIMEOUT)
        return mailing_units

    @staticmethod
    def get_owner_mailing_units(owner_id):
        if not CACHE_ENABLED:
            return MailingUnit.objects.filter(owner_id=owner_id)
        key = f"owner_mailing_units_{owner_id}"
        mailing_units = cache.get(key)
        if mailing_units is not None:
            return mailing_units
        mailing_units = MailingUnit.objects.filter(owner_id=owner_id)
        cache.set(key, mailing_units, CACHE_TIMEOUT)
        return mailing_units

    @staticmethod
    def get_all_launched_mailing_units():
        if not CACHE_ENABLED:
            return MailingUnit.objects.filter(status="Launched")
        key = "launched_mailing_units"
        mailing_units = cache.get(key)
        if mailing_units is not None:
            return mailing_units
        mailing_units = MailingUnit.objects.filter(status="Launched")
        cache.set(key, mailing_units, CACHE_TIMEOUT)
        return mailing_units

    @staticmethod
    def get_owner_launched_mailing_units(owner_id):
        if not CACHE_ENABLED:
            return MailingUnit.objects.filter(owner_id=owner_id, status="Launched")
        key = f"owner_launched_mailing_units_{owner_id}"
        mailing_units = cache.get(key)
        if mailing_units is not None:
            return mailing_units
        mailing_units = MailingUnit.objects.filter(owner_id=owner_id, status="Launched")
        cache.set(key, mailing_units, CACHE_TIMEOUT)
        return mailing_units



class MessageService:

    @staticmethod
    def get_owner_messages(owner_id):
        if not CACHE_ENABLED:
            return Message.objects.filter(owner_id=owner_id)
        key = f"owner_messages_{owner_id}"
        messages = cache.get(key)
        if messages is not None:
            return messages
        messages = Message.objects.filter(owner_id=owner_id)
        cache.set(key, messages, CACHE_TIMEOUT)
        return messages


class MailReceiverService:

    @staticmethod
    def get_all_mail_receivers():
        if not CACHE_ENABLED:
            return MailReceiver.objects.all()
        key = "mail_receivers"
        mail_receivers = cache.get(key)
        if mail_receivers is not None:
            return mail_receivers
        mail_receivers = MailReceiver.objects.all()
        cache.set(key, mail_receivers, CACHE_TIMEOUT)
        return mail_receivers

    @staticmethod
    def get_owner_mail_receivers(owner_id):
        if not CACHE_ENABLED:
            return MailReceiver.objects.filter(owner_id=owner_id)
        key = f"owner_mail_receivers_{owner_id}"
        mail_receivers = cache.get(key)
        if mail_receivers is not None:
            return mail_receivers
        mail_receivers = MailReceiver.objects.filter(owner_id=owner_id)
        cache.set(key, mail_receivers, CACHE_TIMEOUT)
        return mail_receivers


class MailingAttemptService:

    @staticmethod
    def get_mailing_attempts_by_mailing(mailing_id):
        if not CACHE_ENABLED:
            return MailingAttempt.objects.filter(mailing=mailing_id)
        key = f"mailing_attempts_{mailing_id}"
        mailing_attempts = cache.get(key)
        if mailing_attempts is not None:
            return mailing_attempts
        mailing_attempts = MailingAttempt.objects.filter(mailing=mailing_id)
        cache.set(key, mailing_attempts, CACHE_TIMEOUT)
        return mailing_attempts

    @staticmethod
    def get_mailing_attempts_by_owner(owner):
        if not CACHE_ENABLED:
            return MailingAttempt.objects.filter(owner=owner)
        key = f"mailing_attempts_{owner}"
        mailing_attempts = cache.get(key)
        if mailing_attempts is not None:
            return mailing_attempts
        mailing_attempts = MailingAttempt.objects.filter(mailing__owner=owner)
        cache.set(key, mailing_attempts, CACHE_TIMEOUT)
        return mailing_attempts

    @staticmethod
    def get_mailing_attempts_by_status(owner, status):
        if not CACHE_ENABLED:
            return MailingAttempt.objects.filter(status=status, mailing__owner=owner)
        key = f"mailing_attempts_{owner}_{status}"
        mailing_attempts = cache.get(key)
        if mailing_attempts is not None:
            return mailing_attempts
        mailing_attempts = MailingAttempt.objects.filter(status=status, mailing__owner=owner)
        cache.set(key, mailing_attempts, CACHE_TIMEOUT)
        return mailing_attempts