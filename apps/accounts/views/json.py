from apps.core.helpers import render_to_json
from apps.accounts.models import User


@render_to_json()
def users(request):
    q = request.GET.get('q')
    if not q:
        return []
    users = User.objects.filter(username__icontains=q)
    _users = []
    for user in users:
        _users.append({'username': user.username, 'pk': user.pk})
    return _users
