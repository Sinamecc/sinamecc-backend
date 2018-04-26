#!/bin/bash
export DJANGO_SETTINGS_MODULE=config.settings.local_sqlite
python manage.py migrate
python manage.py runserver
