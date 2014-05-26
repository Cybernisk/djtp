DJango Template Project
=======================
.. image:: https://travis-ci.org/tarvitz/djtp.svg?branch=master
    :target: https://travis-ci.org/tarvitz/djtp


* DJTP means Django template project

**DJTP** *serves* for quick/fast your django application make start.

.. contents:: :local:
    :depth: 2

License
~~~~~~~
minified BSD license you can find inside LICENSE file

Common features
~~~~~~~~~~~~~~~
It's standard django application with small and simple dependencies and some
bunch of helper code which (app) allows you to make your own project a little bit faster.


Backend dependecies (requirements/base.txt)
```````````````````````````````````````````
* Django 1.6+
* South 0.8.2+
* pytz 2013.8+
* simplejson 3.3.0

All backend dependencies you can installed via pip using:
.. code-block::

    user@localhost$ pip install -r requirements/base.txt

Frontend dependecies
````````````````````
* bootstrap 3.0+,
* jquery 1.8.3+,
* select2 3.4.3+
* noty 2.1.0+

All frontend dependencies you can installed via ``bower`` (it depens on nodejs 0.10+) using:
.. code-block::

    # you should run this command in project root directory
    user@localhost$ bower install


Installation
~~~~~~~~~~~~
For general installation you would probably need virtual environment with pip
installed:

Python 2.7
``````````
.. code-block:: bash

   user@localhost$ virtualenv --no-site-packages venv
   user@localhost$ source venv/bin/activate
   user@localhost$ pip install -r requirements/base.txt

*optional*

.. code-block:: bash

   user@localhost$ pip install -r requirements/docs.txt

Python 3.3
``````````
document build requirements stored in base-py3.txt

.. code-block:: bash
   user@localhost$ virtualenv --no-site-packages venv3
   user@localhost$ source venv3/bin/activate
   user@localhost$ pip install -r requirements/py3.txt



Tests
~~~~~
You could run tests via `python manage.py test --settings=app.settings.test `
or via `./scripts/run_tests.sh` script

.. code-block:: bash

   user@localhost$ ./scripts/run_tests.sh apps.accounts

First run
~~~~~~~~~
After dependecies were installed you should build your own
database/database file (if you decided use sqlite3)

.. code-block:: bash

    (venv) user@localhost$ python ./manage.py syncdb

Then compile project bootstrap markup using less compiler (tested with nodejs lessc)
or run `./scripts/update_styles.sh` script

.. code-block:: bash
    (venv) user@localhost$ lessc --yui-compress --no-color media/less/bootstrap.less > media/css/bootstrap.css


Documentation
~~~~~~~~~~~~~
Whole bunch of the docs you can read by clicking this link
`djtp.readthedocs.org <http://djtp.readthedocs.org>`_


Development
~~~~~~~~~~~

.. note::

    There's no certain plan for project development, but every major update of django
    would be integreated into `djtp` as soon as possible.