JsonApp
=======

Puropse
-------
Json app serves as proxy for url scheme and url namespaces already created applications.

Usage
-----

Contents of ``apps/json/urls.py``:

.. code-block:: python

    from django.conf.urls import patterns, include, url

    urlpatterns = patterns(
        '',
        url(r'^accounts/', include('apps.accounts.urls.json',
                                   namespace='accounts')),
    )

Mean application accounts use separate url schema and path for json only request/responses.

**URL-schema usage**:

.. code-block:: django

    {% url "json:accounts:users" %}


Full cycle example
------------------

Lets add some view for serialize get now for given timezone serialized in json and put it into the core application.

**Step 1**

Create json view for serving our future jsons request/responses in any editor/ide you like and put it in ``apps/core``.

Example:``apps/core/json_views.py``

.. code-block:: python

    # coding: utf-8
    from django.http import HttpResponse
    from django.utils.timezone import utc
    from datetime import datetime
    import pytz


    def timezone_now(request, domain, zone):
        now = datetime.utcnow().replace(tzinfo=utc)
        response = HttpResponse(content_type='application/json')
        response.write(
            now.astimezone(
                pytz.timezone('{0}/{1}'.format(domain, zone))
            ).ctime()
        )
        return response

**Step 2**

Create separate url schema for its view in ``apps/core/json_urls.py``. You can assign any name you like
for json urls file.

Example:``apps/core/json_urls.py``

.. code-block:: python

    from django.conf.urls import patterns, url

    urlpatterns = patterns(
        'apps.core.json_views',
        url(r'^timezone/(?P<domain>[\w\-_]+)/(?P<zone>[\w\-_]+)/$', 'timezone_now',
            name='timezone-now'),
    )

**Step 3**

Include created schemas to jsonapp urls

.. code-block:: python

    url(r'^core/', include('apps.core.json_urls', namespace='core'))

Now we can fully use created ``timezone_now`` view via separate json url schema:

.. code-block:: django

    $.getJSON('{% url "json:core:timezone-now" %}', function(json){
        console.log(json);
    });

