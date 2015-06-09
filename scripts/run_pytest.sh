#!/bin/bash
ALLURE=`which allure.sh`
COV=`which coverage`
PYTHONPATH=$PWD $COV run --source=apps -m py.test --alluredir=db/reports/allure apps/
if [ ! -z $ALLURE ]; then
    echo "building allure reports"
    if [ ! $? -eq 0 ]; then
        $ALLURE generate generate db/reports/allure/ -o db/reports/reports -v 1.4.11
    fi
fi
echo "building coverage reports"
$COV html
