# coding: utf-8
from django.http import HttpResponse
from django.utils.timezone import utc
from datetime import datetime
import pytz


def timezone_now(request, domain, zone):
    """
    :param request:
    :param domain:
    :param zone:
    :return:
    """
    now = datetime.utcnow().replace(tzinfo=utc)
    response = HttpResponse(content_type='application/json')
    response.write(
        now.astimezone(
            pytz.timezone('{0}/{1}'.format(domain, zone))
        ).ctime()
    )
    return response