"""Signals

.. module:: accounts.signals
   :platform: Linux, Unix
   :synopsis: signals for accounts app

.. moduleauthor:: Nickolas Fox <lilfoxster@gmail.com>
"""

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
    """user pre save signal"""
    return instance


def setup_signals():
    pass