# -*- coding: utf-8 -*-
from django import forms
from django.forms.util import ErrorList
from django.utils.translation import ugettext_lazy as _
from apps.core.forms import RequestFormMixin

from django.contrib import auth

from apps.accounts.models import User
from django.core.exceptions import ImproperlyConfigured
from apps.accounts.models import UserSID


class LoginForm(forms.Form):
    username = forms.CharField(label=_("Username"))
    password = forms.CharField(
        label=_("Password"), widget=forms.PasswordInput())

    def clean(self):
        cd = self.cleaned_data
        username = cd.get('username')
        password = cd.get('password')

        user = auth.authenticate(username=username, password=password)
        if not user:
            # fail to authenticate, probably incorrect auth data
            msg = _("Sorry your username or/and password are invalid")
            self._errors['password'] = ErrorList([msg])
            if 'password' in cd:
                del cd['password']
        
        cd['user'] = user
        return cd


# Yes, I know what I'm doing
# noinspection PyArgumentList,PyUnresolvedReferences
class BruteForceCheckMixin(object):
    """ depends on RequestModelForm """
    def __init__(self, *args, **kwargs):
        super(BruteForceCheckMixin, self).__init__(*args, **kwargs)
        if all(self.data or (None, )):
            if not hasattr(self, 'request'):
                raise ImproperlyConfigured("You should add request")

    def save(self, commit=True):
        instance = super(BruteForceCheckMixin, self).save(commit)
        if 'brute_force_iter' in self.request.session:
            del self.request.session['brute_force_iter']
            self.request.session.save()
        return instance

    def is_valid(self, *args, **kwargs):
        is_valid = super(BruteForceCheckMixin, self).is_valid(*args, **kwargs)
        if not is_valid:
            self.request['brute_force_iter'] = \
                self.request.get('brute_force_iter', 0) + 1
        return is_valid


class PasswordRestoreInitiateForm(forms.Form):
    email = forms.CharField(
        label=_("Email"), help_text=_("Your email")
    )

    def clean_email(self):
        email = self.cleaned_data['email'] or None
        users = User.objects.filter(email__iexact=email)
        if not users:
            raise forms.ValidationError(
                _("Users with given email does not exists")
            )
        self.cleaned_data['users'] = users
        return email


class PasswordRestoreForm(RequestFormMixin,
                          BruteForceCheckMixin,
                          forms.ModelForm):
    password = forms.CharField(
        label=_("Password"), widget=forms.PasswordInput()
    )
    password2 = forms.CharField(
        label=_("Password repeat"), widget=forms.PasswordInput()
    )

    def clean(self):
        cd = self.cleaned_data
        password = cd['password']
        password2 = cd['password2']
        if all((password, password2) or (None, )):
            if password != password2:
                msg = _("Passwords don't match")
                self._errors['password'] = ErrorList([msg])
        return cd

    def save(self, commit=True):
        user = self.instance.user
        user.set_password(self.cleaned_data['password'])
        user.save()
        instance = self.instance
        if commit:
            self.instance.expired = True
            self.instance.save()
            instance = self.instance
        else:
            instance.expired = True
            instance = super(PasswordRestoreForm, self).save(commit=commit)

        return instance

    class Meta:
        model = UserSID
        exclude = ('expired_date', 'expired', 'sid', 'user')


class PasswordChangeForm(forms.ModelForm):
    required_css_class = 'required'
    old_password = forms.CharField(
        required=True,
        label=_("Old password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password_repeat = forms.CharField(
        label=_("New password repeat"),
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean(self):
        cd = self.cleaned_data
        old_password = cd.get('old_password')
        new_pwd = cd.get('new_password')
        new_pwd_repeat = cd.get('new_password_repeat')
        if not old_password:
            return cd
        user = auth.authenticate(
            username=self.instance.username, password=old_password
        )
        if not user:
            msg = _("Old password does not match")
            self._errors['old_password'] = ErrorList([msg])
            if 'old_password' in cd:
                cd.pop('old_password')
        if all((new_pwd, new_pwd_repeat) or (None, )):
            if new_pwd != new_pwd_repeat:
                msg = _("Passwords don't match")
                self._errors['new_password'] = ErrorList([msg])
                if 'new_password' in cd:
                    cd.pop('new_password')
        return cd

    def save(self, commit=True):
        self.instance.set_password(self.cleaned_data['new_password'])
        self.instance.save()
        super(PasswordChangeForm, self).save(commit)

    class Meta:
        model = User
        fields = []
