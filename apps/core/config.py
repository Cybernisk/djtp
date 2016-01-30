# -*- coding: utf-8 -*-
"""
.. module:: apps.core.app_config
    :synopsis: App config
    :platform: Linux, Unix, Windows
.. moduleauthor:: Nickolas Fox <tarvitz@blacklibary.ru>
.. sectionauthor:: Nickolas Fox <tarvitz@blacklibary.ru>
"""

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


__LICENSE__ = "BSD"
__AUTHOR__ = "Nickolas Fox"
__EMAIL__ = "tarvitz@blacklibrary.ru"


class CoreConfig(AppConfig):
    name = 'apps.core'
    label = 'core'
    verbose_name = _('Core Application Module')

    def ready(self):
        """
        setup actions
        """
