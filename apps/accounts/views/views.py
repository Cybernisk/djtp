"""An account classed based views.

.. module:: account.views
   :platform: Linux, Unix
   :synopsis: Classed based views for accounts handling operations
.. moduleauthor:: Nickolas Fox <lilfoxster@gmail.com>

"""
# -*- coding: utf-8 -*-

from apps.core.helpers import render_to, get_object_or_None
from django.contrib.auth.decorators import login_required
from apps.accounts.decorators import prevent_bruteforce
from django.http import Http404
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.views import generic
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from apps.accounts.models import UserSID, User
from apps.core.views import LoginRequiredMixin

from apps.accounts.forms import (
    LoginForm, PasswordRestoreInitiateForm, PasswordChangeForm,
    PasswordRestoreForm
)
from django.contrib import auth


class LoginView(generic.FormView):
    """LoginView"""
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('core:index')

    def form_valid(self, form):
        form_valid = super(LoginView, self).form_valid(form)
        auth.login(self.request, form.cleaned_data['user'])
        return form_valid


class LogoutView(generic.TemplateView):
    """LogoutView"""
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        return self.render_to_response({})


class PasswordRestoreInitiateView(generic.FormView):
    """Password Restore Initiate View"""
    template_name = 'accounts/password_restore_initiate.html'
    form_class = PasswordRestoreInitiateForm
    success_url = reverse_lazy('accounts:password-restore-initiated')

    def form_valid(self, form):
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
                    user=self.request.user).order_by('-id')[0]
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
        return redirect(self.get_success_url())


class PasswordRestoreView(generic.FormView):
    """Password Restore View"""
    form_class = PasswordRestoreForm
    template_name = 'accounts/password_restore.html'
    success_url = reverse_lazy('accounts:password-restored')

    @method_decorator(prevent_bruteforce)
    def dispatch(self, request, *args, **kwargs):
        return super(PasswordRestoreView, self).dispatch(request,
                                                         *args, **kwargs)

    def get_user_sid_instance(self):
        if not hasattr(self, 'user_sid'):
            self.user_sid = get_object_or_None(
                UserSID, sid=self.kwargs.get('sid', 0), expired=False)
            if not self.user_sid:
                self.request.session['brute_force_iter'] \
                    = self.request.session.get('brute_force_iter', 0) + 1
                self.request.session.save()
                raise Http404("not found")
        return self.user_sid

    def get_form_kwargs(self):
        kwargs = super(PasswordRestoreView, self).get_form_kwargs()
        kwargs.update({
            'instance': self.get_user_sid_instance(),
            'request': self.request
        })
        return kwargs

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())


class PasswordChangeView(LoginRequiredMixin, generic.FormView):
    """Password Change View"""
    form_class = PasswordChangeForm
    model = User
    success_url = reverse_lazy('accounts:password-changed')
    template_name = 'accounts/password_change.html'

    def get_form_kwargs(self):
        kwargs = super(PasswordChangeView, self).get_form_kwargs()
        kwargs.update({
            'instance': self.request.user
        })
        return kwargs

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())


class ProfileView(LoginRequiredMixin, generic.TemplateView):
    """Profile View"""
    template_name = 'accounts/profile.html'