import re
import pytz

from django.db import models
from django.core import validators
from django.utils import timezone
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, UserManager
)

from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from apps.accounts.managers import UserSIDManager
from datetime import datetime, timedelta
from django.conf import settings

# Create your models here.


class User(PermissionsMixin, AbstractBaseUser):
    #is_admin = models.BooleanField(
    #    _("is_admin"), default=False,
    #)
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(_('username'), max_length=50, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                _('Enter a valid username.'), 'invalid')
        ])
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    # extensions
    tz = models.CharField(
        _('tz'), help_text=_("user time zone"),
        max_length=64, default='UTC',
        choices=zip(pytz.all_timezones, pytz.all_timezones)
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __unicode__(self):
        return self.username

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    # urls
    def get_profile_url(self):
        return reverse_lazy('accounts:profile')

    def get_recover_password_url(self):
        return reverse_lazy('accounts:password-restore-initiate')

    def get_change_password_url(self):
        return reverse_lazy('accounts:password-change')

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class UserSID(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_sid_set')
    sid = models.CharField(_("SID"), unique=True, max_length=512)
    # additional fields ?
    expired_date = models.DateTimeField(
        _("Expires"),
        default=timezone.now() + timedelta(weeks=1)
    )
    expired = models.BooleanField(
        _("expired?"), default=False
    )
    created_on = models.DateTimeField(
        _("created on"),
        default=timezone.now,
        auto_now=True
    )
    updated_on = models.DateTimeField(
        _('updated on'),
        default=timezone.now,
        auto_now_add=True
    )
    objects = UserSIDManager()

    def __unicode__(self):
        return "%s [%s]" % (self.user.username, self.sid)

    class Meta:
        verbose_name = _("UserSID")
        verbose_name_plural = _("UserSIDs")


from .signals import *
setup_signals()
