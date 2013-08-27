# Create your views here.
# -*- coding: utf-8 -*-
from apps.core.helpers import render_to, get_object_or_None
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import prevent_bruteforce
from django.http import Http404
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from apps.accounts.models import UserSID

from apps.accounts.forms import (
    LoginForm, PasswordRestoreInitiateForm, PasswordChangeForm,
    PasswordRestoreForm
)

from django.contrib import auth

@render_to('accounts/login.html')
def login(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.cleaned_data['user']
            auth.login(request, user)
            return {'redirect': 'core:index'}
    return {
        'form': form
    }


@render_to('index.html')
def logout(request):
    auth.logout(request)
    return {}


@render_to('accounts/password_restore_initiate.html')
def password_restore_initiate(request):
    form = PasswordRestoreInitiateForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            users = form.cleaned_data['users']
            sids = UserSID.objects.filter(user__in=users, expired=True)

            sids = []
            if not sids:
                for user in users:
                    sid = UserSID.objects.create(user)
                    sids.append(sid)
            else:
                for user in users:
                    sid = UserSID.objects.filter(
                        user=request.user).order_by('-id')[0]
                    sids.append(sid)

            for sid in sids:
                msg = settings.PASSWORD_RESTORE_REQUEST_MESSAGE % {
                    'link': settings.SITE_URL + reverse(
                    'accounts:password-restore', args=(sid.sid, )),
                    'url': settings.CONTACT_URL
                }
                send_mail(
                    subject=unicode(_('Your password requested to change')),
                    message=unicode(msg),
                    from_email=settings.EMAIL_FROM,
                    recipient_list=[sid.user.email]
                )
            return {'redirect': 'accounts:password-restore-initiated'}
    return {'form': form}


@prevent_bruteforce
@render_to('accounts/password_restore.html')
def password_restore(request, sid):
    instance = get_object_or_None(UserSID, sid=sid, expired=False)
    if not instance:
        request.session['brute_force_iter'] \
            = request.session.get('brute_force_iter', 0) + 1
        raise Http404("not found")

    form = PasswordRestoreForm(
        request.POST or None, instance=instance, request=request
    )
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return {'redirect': 'accounts:password-restored'}
    return {'form': form}


@login_required
@render_to('accounts/password_change.html')
def password_change(request):
    form = PasswordChangeForm(request.POST or None, instance=request.user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return {'redirect': 'accounts:password-changed'}
    return {'form': form}
