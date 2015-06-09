"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from datetime import datetime
import pytz

from django.test import TestCase
from django.conf import settings
from django.template import Template, Context
from django.utils.unittest import skipIf
from django.contrib.contenttypes.models import ContentType
from django.http import Http404

from apps.core import helpers

import allure
from allure.constants import Severity


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
                print("Got %(err)s in %(key)s" % msg)
            raise AssertionError


@allure.feature("Apps: core")
class TimezonesTest(TestHelperMixin, TestCase):
    def setUp(self):
        pass

    @skipIf(not settings.USE_TZ, "should be tz seuses")
    @allure.story('timezone')
    @allure.severity(Severity.CRITICAL)
    def test_gmt_timezone(self):
        london = datetime.utcnow().replace(
            tzinfo=pytz.timezone('Europe/London'))
        moscow = datetime.utcnow().replace(
            tzinfo=pytz.timezone('Europe/Moscow'))

        self.assertEqual(moscow.tzinfo, pytz.timezone('Europe/Moscow'))
        self.assertEqual(london.tzinfo, pytz.timezone('Europe/London'))


@allure.feature('Apps: Core')
class TestTemplateTags(TestCase):

    def setUp(self):
        self.get_form_template = """
        {% load coretags %}
        {% get_form 'apps.accounts.forms.LoginForm' as form %}
        {{ form.as_ul }}
        """

    @allure.story('templatetags')
    @allure.severity(Severity.CRITICAL)
    def test_get_form(self):
        template = Template(self.get_form_template)
        c = Context()
        html = template.render(c)
        self.assertInHTML(
            '<input id="id_username" name="username" type="text" />',
            html
        )


class A(object):
    pass


class B(object):
    pass


@allure.feature('Apps: Core')
class TestHelpers(TestCase):
    @allure.story('helpers')
    @allure.severity(Severity.NORMAL)
    def test_safe_ret(self):
        """
        safe ret
        """
        test_instance = A()
        test_instance.b = B()
        test_instance.b.a = A()

        self.assertIsInstance(helpers.safe_ret(test_instance, 'b.a'), A)
        self.assertIsInstance(helpers.safe_ret(test_instance, 'b'), B)

    @allure.story('helpers')
    @allure.severity(Severity.NORMAL)
    def test_get_int_or_zero(self):
        self.assertEqual(helpers.get_int_or_zero('test'), 0)
        self.assertEqual(helpers.get_int_or_zero('12'), 12)

    @allure.story('helpers')
    @allure.severity(Severity.NORMAL)
    def test_get_content_type(self):
        ct = ContentType.objects.latest('pk')
        with allure.step('with basestring'):
            self.assertIsInstance(
                helpers.get_content_type('contenttypes.contenttype'),
                ContentType
            )
        with allure.step('with instance'):
            self.assertIsInstance(
                helpers.get_content_type(ct),
                ContentType
            )
        with allure.step('with model class'):
            self.assertIsInstance(
                helpers.get_content_type(ContentType),
                ContentType
            )

    @allure.story('helpers')
    @allure.severity(Severity.NORMAL)
    def test_get_content_type_or_None(self):
        with allure.step('get'):
            self.assertIsInstance(
                helpers.get_content_type_or_None('contenttypes.contenttype'),
                ContentType
            )
        with allure.step('get None'):
            self.assertIsNone(
                helpers.get_content_type_or_None('contenttypes.nonexistent')
            )

    @allure.story('helpers')
    @allure.severity(Severity.NORMAL)
    def test_get_content_type_or_404(self):
        with allure.step('get'):
            self.assertIsInstance(
                helpers.get_content_type_or_404('contenttypes.contenttype'),
                ContentType
            )
        with allure.step('get None'):
            with self.assertRaises(Http404):
                helpers.get_content_type_or_404('contenttypes.nonexistent')
