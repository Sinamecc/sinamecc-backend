FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE config.settings.stage_aws

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /code/

EXPOSE 8015
STOPSIGNAL SIGTERM

ENTRYPOINT exec gunicorn --access-logfile - --log-level debug --workers 3 --bind 0.0.0.0:8015 config.wsgi:application