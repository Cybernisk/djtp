from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser

from django.utils.translation import ugettext_lazy as _
from apps.accounts.managers import UserSIDManager
from datetime import datetime, timedelta
from django.conf import settings

# Create your models here.


class User(AbstractUser):
    #is_admin = models.BooleanField(
    #    _("is_admin"), default=False,
    #)
    #USERNAME_FIELD = 'username'
    #REQUIRED_FIELDS = ['username', 'email']

    def __unicode__(self):
        return self.username

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class UserSID(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_sid_set')
    sid = models.CharField(_("SID"), unique=True, max_length=512)
    # additional fields ?
    expired_date = models.DateTimeField(
        _("Expires"), default=datetime.now() + timedelta(weeks=1)
    )
    expired = models.BooleanField(
        _("expired?"), default=False
    )
    created_on = models.DateTimeField(
        _("created on"), default=datetime.now,
        auto_now=True
    )
    updated_on = models.DateTimeField(
        _('updated on'), default=datetime.now,
        auto_now_add=True
    )
    objects = UserSIDManager()

    def __unicode__(self):
        return "%s [%s]" % (self.user.username, self.sid)

    class Meta:
        verbose_name = _("UserSID")
        verbose_name_plural = _("UserSIDs")


from .signals import *
