"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from datetime import datetime
import pytz

from django.utils import timezone
from django.test import TestCase
from django.conf import settings
from django.utils.unittest import skipIf


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class TestHelperMixin(object):
    def login(self, user):
        if user:
            logged = self.client.login(username=user, password='123456')
            self.assertEqual(logged, True)
        else:
            self.client.logout()

    def check_state(self, instance, data, check=lambda x: x, check_in=None):
        messages = []
        check_in = check_in or self.assertIn
        for (key, value) in data.items():
            try:
                if hasattr(getattr(instance, key), 'all'):
                    for field in getattr(instance, key).all():
                        check_in(field, value)
                else:
                    check(getattr(instance, key), value)
            except AssertionError as err:
                messages.append({
                    'err': err,
                    'key': key
                })
        if messages:
            for msg in messages:
                print "Got %(err)s in %(key)s" % msg
            raise AssertionError


class TimezonesTest(TestHelperMixin, TestCase):
    def setUp(self):
        pass

    @skipIf(not settings.USE_TZ, "should be tz seuses")
    def test_gmt_timezone(self):
        london = datetime.utcnow().replace(
            tzinfo=pytz.timezone('Europe/London'))
        moscow = datetime.utcnow().replace(
            tzinfo=pytz.timezone('Europe/Moscow'))

        self.assertEqual(moscow.tzinfo, pytz.timezone('Europe/Moscow'))
        self.assertEqual(london.tzinfo, pytz.timezone('Europe/London'))