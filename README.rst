DJango Template Project
=======================
.. image:: https://travis-ci.org/tarvitz/djtp.svg?branch=master
    :target: https://travis-ci.org/tarvitz/djtp

.. image:: https://coveralls.io/repos/tarvitz/djtp/badge.svg
  :target: https://coveralls.io/r/tarvitz/djtp


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
* Django 1.8+
* pytz 2015.4+
* simplejson 3.7.3

All backend dependencies you can installed via pip using:
.. code-block::

    user@localhost$ pip install -r requirements/base.txt

Frontend dependecies
````````````````````
* bootstrap 3.3+,
* jquery 2.1+,
* select2 4.0+
* noty 2.3.5+

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

Py.Test
~~~~~~~
Use allure and pytest for better reports generating:

.. code-block:: bash

  user@localhost$ ./scripts/run_pytest.sh

Coverage
~~~~~~~~
with py.test you could use pytest-cov (code coverage) to generate stats around
your code being tests with unit tests.

.. code-block:: bash

  user@localhost$ coverage run --source=apps -m py.test --alluredir=db/reports/allure apps/
  user@localhost$ coverage report --fail-under=90
  user@localhist$ coverage html

First run
~~~~~~~~~
After dependecies were installed you should build your own
database/database file (if you decided use sqlite3)

.. code-block:: bash
    (venv) user@localhost$ mkdir db
    (venv) user@localhost$ python ./manage.py syncdb --migrate

Also you should install `bower <https://www.npmjs.org/package/bower>`_ dependencies.
``Bower`` is a nodejs package that serves for frontend dependecies package manager.

.. code-block:: bash

    user@localhost$ sudo npm install -g bower
    # or
    root@localhost$ npm install -g bower
    # then from ``project root`` directory run
    user@localhost$ bower install

After all frontend dependencies installation some git submodules should be reinitialized for
current project version:

.. code-block:: bash

    $ git submodule
    48cd4b44bc94046cab20e0d345c978483684ab2e media/less/select2-bootstrap-css (v1.0-198-g48cd4b4)
    $ git submodule init media/less/select2-bootstrap-css
    $ git submodule update media/less/select2-bootstrap-css

After successfull submodule update the last step is to compile bootstrap less into css file.

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