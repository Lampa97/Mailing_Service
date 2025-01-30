from django.core.cache import cache

from config.settings import CACHE_ENABLED

from .models import MailingAttempt, MailingUnit, MailReceiver, Message

CACHE_TIMEOUT = 60


def count_total(queryset, count):
    """Return the total count of the queryset if count is True, otherwise return the queryset itself."""
    return queryset.count() if count else queryset


class MailingUnitService:

    @staticmethod
    def get_all_mailing_units(count=False):
        """Return all mailing units if count is False otherwise return total amount of queried mailing units."""
        if not CACHE_ENABLED:
            mailing_units = MailingUnit.objects.all()
            return count_total(mailing_units, count)
        key = "mailing_units"
        mailing_units = cache.get(key)
        if mailing_units is not None:
            return count_total(mailing_units, count)
        mailing_units = MailingUnit.objects.all()
        cache.set(key, mailing_units, CACHE_TIMEOUT)
        return count_total(mailing_units, count)

    @staticmethod
    def get_owner_mailing_units(owner_id, count=False):
        """Return all mailing units of the owner if count is False
        otherwise return total amount of queried mailing units."""
        if not CACHE_ENABLED:
            mailing_units = MailingUnit.objects.filter(owner_id=owner_id)
            return count_total(mailing_units, count)
        key = f"owner_mailing_units_{owner_id}"
        mailing_units = cache.get(key)
        if mailing_units is not None:
            return count_total(mailing_units, count)
        mailing_units = MailingUnit.objects.filter(owner_id=owner_id)
        cache.set(key, mailing_units, CACHE_TIMEOUT)
        return count_total(mailing_units, count)

    @staticmethod
    def get_all_launched_mailing_units(count=False):
        """Return all launched mailing units if count is False
        otherwise return total amount of queried mailing units."""
        if not CACHE_ENABLED:
            mailing_units = MailingUnit.objects.filter(status="Launched")
            return count_total(mailing_units, count)
        key = "launched_mailing_units"
        mailing_units = cache.get(key)
        if mailing_units is not None:
            return count_total(mailing_units, count)
        mailing_units = MailingUnit.objects.filter(status="Launched")
        cache.set(key, mailing_units, CACHE_TIMEOUT)
        return count_total(mailing_units, count)

    @staticmethod
    def get_owner_launched_mailing_units(owner_id, count=False):
        """Return all launched mailing units of the owner if count is False
        otherwise return total amount of queried mailing units."""
        if not CACHE_ENABLED:
            mailing_units = MailingUnit.objects.filter(owner_id=owner_id, status="Launched")
            return count_total(mailing_units, count)
        key = f"owner_launched_mailing_units_{owner_id}"
        mailing_units = cache.get(key)
        if mailing_units is not None:
            return count_total(mailing_units, count)
        mailing_units = MailingUnit.objects.filter(owner_id=owner_id, status="Launched")
        cache.set(key, mailing_units, CACHE_TIMEOUT)
        return count_total(mailing_units, count)


class MessageService:

    @staticmethod
    def get_owner_messages(owner_id):
        """Return all messages of the owner."""
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
    def get_all_mail_receivers(count=False):
        """Return all mail receivers if count is False
        otherwise return total amount of queried mail receivers."""
        if not CACHE_ENABLED:
            mail_receivers = MailReceiver.objects.all()
            return count_total(mail_receivers, count)
        key = "mail_receivers"
        mail_receivers = cache.get(key)
        if mail_receivers is not None:
            return count_total(mail_receivers, count)
        mail_receivers = MailReceiver.objects.all()
        cache.set(key, mail_receivers, CACHE_TIMEOUT)
        return count_total(mail_receivers, count)

    @staticmethod
    def get_owner_mail_receivers(owner_id, count=False):
        """Return all mail receivers of the owner if count is False
        otherwise return total amount of queried mail receivers."""
        if not CACHE_ENABLED:
            mail_receivers = MailReceiver.objects.filter(owner_id=owner_id)
            return count_total(mail_receivers, count)
        key = f"owner_mail_receivers_{owner_id}"
        mail_receivers = cache.get(key)
        if mail_receivers is not None:
            return count_total(mail_receivers, count)
        mail_receivers = MailReceiver.objects.filter(owner_id=owner_id)
        cache.set(key, mail_receivers, CACHE_TIMEOUT)
        return count_total(mail_receivers, count)


class MailingAttemptService:

    @staticmethod
    def get_mailing_attempts_by_mailing(mailing_id, count=False):
        """Return all mailing attempts of the mailing if count is False
        otherwise return total amount of queried mailing attempts."""
        if not CACHE_ENABLED:
            mailing_attempts = MailingAttempt.objects.filter(mailing=mailing_id)
            return count_total(mailing_attempts, count)
        key = f"mailing_attempts_{mailing_id}"
        mailing_attempts = cache.get(key)
        if mailing_attempts is not None:
            return count_total(mailing_attempts, count)
        mailing_attempts = MailingAttempt.objects.filter(mailing=mailing_id)
        cache.set(key, mailing_attempts, CACHE_TIMEOUT)
        return count_total(mailing_attempts, count)

    @staticmethod
    def get_mailing_attempts_by_owner(owner, count=False):
        """Return all mailing attempts of the owner if count is False
        otherwise return total amount of queried mailing attempts."""
        if not CACHE_ENABLED:
            mailing_attempts = MailingAttempt.objects.filter(owner=owner)
            return count_total(mailing_attempts, count)
        key = f"mailing_attempts_{owner}"
        mailing_attempts = cache.get(key)
        if mailing_attempts is not None:
            return count_total(mailing_attempts, count)
        mailing_attempts = MailingAttempt.objects.filter(mailing__owner=owner)
        cache.set(key, mailing_attempts, CACHE_TIMEOUT)
        return count_total(mailing_attempts, count)

    @staticmethod
    def get_mailing_attempts_by_status(owner, status, count=False):
        """Return all mailing attempts of the owner with the specified status if count is False
        otherwise return total amount of queried mailing attempts."""
        if not CACHE_ENABLED:
            mailing_attempts = MailingAttempt.objects.filter(status=status, mailing__owner=owner)
            return count_total(mailing_attempts, count)
        key = f"mailing_attempts_{owner}_{status}"
        mailing_attempts = cache.get(key)
        if mailing_attempts is not None:
            return count_total(mailing_attempts, count)
        mailing_attempts = MailingAttempt.objects.filter(status=status, mailing__owner=owner)
        cache.set(key, mailing_attempts, CACHE_TIMEOUT)
        return count_total(mailing_attempts, count)
