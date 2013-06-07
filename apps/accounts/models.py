from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser
from django.utils.translation import ugettext_lazy as _

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


from signals import *
