#!/bin/bash
python manage.py test --settings=app.settings.test $@
coverage report --fail-under=90
