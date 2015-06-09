# coding: utf-8
#from django.utils import unittest
import os
import six
import re
from apps.core.tests import TestHelperMixin
from django.test import TestCase
from apps.accounts.models import User
from django.core.urlresolvers import reverse
from apps.core.helpers import get_object_or_None
from copy import deepcopy
from django.core import mail
from django.utils.translation import ugettext_lazy as _
from django.utils.unittest import skipIf

from django.conf import settings
try:
    import simplejson as json
except ImportError:
    import json

try:
    import allure
except ImportError:
    allure = None


class JustTest(TestHelperMixin, TestCase):
    fixtures = [
        'tests/fixtures/load_users.json',
    ]

    password_change_post = {
        'old_password': '123456',
        'new_password': '654321',
        'new_password_repeat': '654321'
    }
    username_login = {
        'username': 'user',
        'password': '123456'
    }
    email_login = {
        'username': 'user@blacklibrary.ru',
        'password': '123456'
    }

    def setUp(self):
        self.urls_void = [
        ]
        self.urls_registered = [
        ]
        self.get_object = get_object_or_None
        self.user = User.objects.get(username='user')
        self.login_url = reverse('accounts:login')

    def test_registered_urls(self):
        messages = []
        for user in ('admin', 'user'):
            logged = self.client.login(username=user, password='123456')
            self.assertEqual(logged, True)
            for url in self.urls_registered:
                response = self.client.get(url, follow=True)
                try:
                    self.assertEqual(response.status_code, 200)
                except AssertionError as err:
                    messages.append({
                        'user': user, 'err': err, 'url': url
                    })
        if messages:
            for msg in messages:
                print ("Got assertion on %(url)s with %(user)s: %(err)s" % msg)
            raise AssertionError

    def tearDown(self):
        pass

    def check_state(self, instance, data, check=lambda x: x):
        messages = []
        for (key, value) in data.items():
            try:
                check(getattr(instance, key), value)
            except AssertionError as err:
                messages.append({
                    'err': err,
                    'key': key
                })
        if messages:
            for msg in messages:
                print ("Got %(err)s in %(key)s" % msg)
            raise AssertionError

    def test_login(self):
        login = self.username_login
        user = User.objects.get(username=self.username_login['username'])
        url = reverse('accounts:login')
        response = self.client.post(url, login, follow=True)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(response.context['user'].is_authenticated(), True)
        self.assertEqual(response.context['user'], user)

    @skipIf(('apps.accounts.backends.EmailAuthBackend'
             not in settings.AUTHENTICATION_BACKENDS),
            "EmailAuthBackend isn't enabled")
    def test_login_by_email(self):
        user = User.objects.get(email=self.email_login['username'])
        url = reverse('accounts:login')
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        context = response.context
        self.assertEqual(context['user'].is_authenticated(), False)

        # login
        response = self.client.post(url, self.email_login, follow=True)
        self.assertEqual(response.status_code, 200)
        context = response.context
        self.assertEqual(context['user'].is_authenticated(), True)
        self.assertEqual(context['user'], user)

    def test_logout(self):
        pass

    def test_password_change(self):
        self.login('user')
        url = self.user.get_change_password_url()

        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, self.password_change_post,
                                    follow=True)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

        login_post = {
            'username': self.user.username,
            'password': self.password_change_post['new_password']
        }
        response = self.client.post(self.login_url, login_post, follow=True)
        self.assertEqual(response.status_code, 200)
        context = response.context
        self.assertEqual(context['user'].is_authenticated(), True)
        self.assertEqual(context['user'].username, self.user.username)

    def test_password_change_wrong_password(self):
        self.login('user')
        url = self.user.get_change_password_url()
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        password_change_post = deepcopy(self.password_change_post)
        password_change_post.update({
            'old_password': 'wrong password',
        })
        response = self.client.post(url, password_change_post, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)
        form = response.context['form']
        self.assertNotEqual(form.errors, {})

        self.assertEqual(form.errors['old_password'][0],
                         six.text_type(_("Old password does not match")))
        self.client.logout()

        login_post = {
            'username': self.user.username,
            'password': password_change_post['new_password']
        }
        response = self.client.post(self.login_url, login_post, follow=True)
        self.assertEqual(response.status_code, 200)
        context = response.context
        self.assertEqual(context['user'].is_authenticated(), False)

    def test_password_recover(self):
        self.login(None)  # anonymous here
        pattern = reverse('accounts:password-restore', args=('_sid_', ))
        pattern = pattern.replace('_sid_', r'[\w\d]+')
        # we have no any context within restore url with sid
        # set for user protection, so we'll get it in our mailbox
        reg = re.compile(pattern, re.U | re.I)

        # urls we follow
        initiate_url = reverse('accounts:password-restore-initiate')
        initiated_url = reverse('accounts:password-restore-initiated')
        restored_url = reverse('accounts:password-restored')

        response = self.client.get(initiate_url)
        self.assertEqual(response.status_code, 200)
        post = {
            'email': 'user@blacklibrary.ru'
        }
        response = self.client.post(initiate_url, post, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['get_full_path'], initiated_url)

        # checking outbox
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject,
                         _("Your password requested to change"))
        urls = re.findall(reg, mail.outbox[0].body)
        self.assertEqual(len(urls), 1)
        restore_url = urls[0]

        restore_post = {
            'password': '654321',
            'password2': '654321'
        }
        response = self.client.post(restore_url, restore_post, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['get_full_path'], restored_url)

        # try to login
        login_url = reverse('accounts:login')
        login_post = {
            'username': 'user',
            'password': restore_post['password']
        }
        response = self.client.post(login_url, login_post, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'].is_authenticated(), True)
        # if you have got failure within code placed below
        # please look for username user@blacklibrary.ru email origin
        self.assertEqual(response.context['user'].username, 'user')

    def test_profile_update(self):
        pass

    def test_register(self):
        pass
