#!/bin/bash
if [[ ! -z $1 ]]; then
	export DJANGO_SETTINGS_MODULE=config.settings.$1
else
	export DJANGO_SETTINGS_MODULE=config.settings.local_sqlite
fi;

echo "from django.contrib.auth import get_user_model; User=get_user_model(); User.objects.filter(username='admin').delete(); User.objects.create_superuser('admin', 'admin@example.com', 'cambiame')" | python manage.py shell
