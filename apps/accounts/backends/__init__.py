# coding: utf-8

from apps.accounts.models import User


class EmailAuthBackend(object):
    """
    Email Authentication backend
    Allows a user to sign in using email/password rather than
    a username/password pair
    """

    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        except User.MultipleObjectsReturned:
            user = User.objects.filter(email=username)[0]
            if user.check_password(password):
                return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
