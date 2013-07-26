# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

PASSWORD_RESTORE_REQUEST_MESSAGE = _("""
    Your or somebody else requested password change for this email account.
    If you're not the person who initiated password request procedure, please ignore
    this letter or give a notice for service administration:
    %(url)s

    Your password restore link: %(link)s
""")
