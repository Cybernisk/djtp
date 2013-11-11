from django.db.models.signals import (
    pre_save, post_save, pre_delete
)
from apps.accounts.models import User
from django.dispatch import receiver


__all__ = [
    'user_pre_saved', 'setup_signals'
]


@receiver(pre_save, sender=User)
def user_pre_saved(instance, **kwargs):
    return instance


def setup_signals():
    pass