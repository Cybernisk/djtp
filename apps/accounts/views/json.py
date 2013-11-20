"""JSON module

.. module:: account.views.json
   :platform: Linux, Unix
   :synopsis: JSON views for accounts application

.. moduleauthor:: Nickolas Fox <lilfoxster@gmail.com>
"""

from apps.core.helpers import render_to_json
from apps.accounts.models import User


@render_to_json(content_type='application/javascript')
def users(request):
    """
    Returns users serialized within json

    :param request: HttpRequest
    :return: dict or queryset or model instance
    """
    q = request.GET.get('q')
    if not q:
        return []
    users = User.objects.filter(username__icontains=q)
    return users.values('username', 'pk')