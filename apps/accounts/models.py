"""Models

.. module:: account.models
   :platform: Linux, Unix
   :synopsis: accounts app models

.. moduleauthor:: Nickolas Fox <tarvitz@blacklibrary.ru>
"""
import re
import pytz

from django.db import models
from django.core import validators
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth.models import (
    AbstractBaseUser, UserManager, Permission, Group,
    _user_has_perm, _user_get_all_permissions, _user_has_module_perms
)
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from django.conf import settings

from . import managers


class User(AbstractBaseUser):
    """
    Base class implementing a fully featured User model with
    admin-compliant permissions.

    Username, password and email are required. Other fields are optional.
    """
    username = models.CharField(
        _('username'), max_length=50, unique=True,
        help_text=_('Required. 30 characters or fewer. Letters, numbers and '
                    '@/./+/-/_ characters'),
        validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                _('Enter a valid username.'),
                'invalid'
            )
        ])
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user '
                                               'can log into this '
                                               'admin site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_(
                                        'Designates whether this user '
                                        'should be treated as active. '
                                        'Unselect this instead of '
                                        'deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    # extensions
    tz = models.CharField(
        _('tz'), help_text=_("user time zone"),
        max_length=64, default='UTC',
        choices=zip(pytz.all_timezones, pytz.all_timezones)
    )
    is_superuser = models.BooleanField(
        _('superuser status'), default=False,
        help_text=_('Designates that this user has all permissions without '
                    'explicitly assigning them.'))
    groups = models.ManyToManyField(
        Group, verbose_name=_('groups'),
        blank=True, help_text=_('The groups this user belongs to. A user will '
                                'get all permissions granted to each of '
                                'their groups.'),
        related_name="user_group_set", related_query_name="user")
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'), blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_permission_set", related_query_name="user")

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
        """Returns the short name for the user."""
        return self.first_name

    @staticmethod
    def get_profile_url():
        """returns profile url"""
        return reverse('accounts:profile')

    @staticmethod
    def get_recover_password_url():
        """returns recover password url"""
        return reverse('accounts:password-restore-initiate')

    @staticmethod
    def get_change_password_url():
        """returns change password url"""
        return reverse('accounts:password-change')

    def get_group_permissions(self, obj=None):
        """
        Returns a list of permission strings that this user has through their
        groups. This method queries all available auth backends. If an object
        is passed in, only permissions matching this object are returned.
        """
        permissions = set()
        for backend in auth.get_backends():
            if hasattr(backend, "get_group_permissions"):
                permissions.update(backend.get_group_permissions(self, obj))
        return permissions

    def get_all_permissions(self, obj=None):
        return _user_get_all_permissions(self, obj)

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission. This method
        queries all available auth backends, but returns immediately if any
        backend returns True. Thus, a user who has permission from a single
        auth backend is assumed to have permission in general. If an object is
        provided, permissions for this specific object are checked.
        """

        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Returns True if the user has each of the specified permissions. If
        object is passed, it checks if the user has all required perms for this
        object.
        """
        for perm in perm_list:
            if not self.has_perm(perm, obj):
                return False
        return True

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


class UserSID(models.Model):
    """
    UserSID class for security hashes store, uses for password recover process
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name='user_sid_set')
    sid = models.CharField(_("SID"), unique=True, max_length=255)
    # additional fields ?
    expired_date = models.DateTimeField(
        _("Expires"),
    )
    expired = models.BooleanField(
        _("expired?"), default=False
    )
    created_on = models.DateTimeField(
        _("created on"),
        auto_now=True
    )
    updated_on = models.DateTimeField(
        _('updated on'),
        auto_now_add=True
    )
    objects = managers.UserSIDManager()

    def __unicode__(self):
        return "%s [%s]" % (self.user.username, self.sid)

    class Meta:
        verbose_name = _("UserSID")
        verbose_name_plural = _("UserSIDs")
