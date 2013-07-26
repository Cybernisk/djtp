# coding: utf-8
#from django.utils import unittest
import os
import re
from apps.core.tests import TestHelperMixin
from django.test import TestCase
from apps.accounts.models import User
from django.core.urlresolvers import reverse
from apps.core.helpers import get_object_or_None
from copy import deepcopy
from django.core import mail
from django.utils.translation import ugettext_lazy as _
try:
    import simplejson as json
except ImportError:
    import json


class JustTest(TestHelperMixin, TestCase):
    fixtures = [
        'tests/fixtures/load_users.json',
    ]

    def setUp(self):
        self.urls_void = [
        ]
        self.urls_registered = [
        ]
        self.get_object = get_object_or_None

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
        login = {
            'username': 'user',
            'password': '123456'
        }
        user = User.objects.get(username='user')
        url = reverse('accounts:login')
        response = self.client.post(url, login, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '/logout/')
        self.assertEqual(response.context['user'], user)

    def test_logout(self):
        pass

    def test_password_change(self):
        pass

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
        self.assertEqual(mail.outbox[0].subject, _("Your password requested to change"))
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
