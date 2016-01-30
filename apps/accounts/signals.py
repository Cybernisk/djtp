"""Signals

.. module:: accounts.signals
   :platform: Linux, Unix
   :synopsis: signals for accounts app

.. moduleauthor:: Nickolas Fox <tarvitz@blacklibrary.ru>
"""

from django.db.models.signals import (
    pre_save
)
from django.dispatch import receiver

from . import models

__all__ = [
    'user_pre_saved', 'setup_signals'
]


@receiver(pre_save, sender=models.User)
def user_pre_saved(instance, **kwargs):
    """
    user pre save signal

    :param instance: user instance
    :type instance: apps.accounts.models.User
    :rtype: apps.accounts.models.User
    :return: user instance
    """
    return instance


def setup_signals():
    """
    setups signals
    """
