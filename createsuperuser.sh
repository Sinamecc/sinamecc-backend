#!/bin/bash
export DJANGO_SETTINGS_MODULE=config.settings.local_sqlite
echo "from django.contrib.auth.models import User; User.objects.filter(username='admin').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'cambiame')" | python manage.py shell
