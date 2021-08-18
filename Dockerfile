FROM python:3.9

ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /code/

EXPOSE 80
STOPSIGNAL SIGTERM

ENTRYPOINT exec gunicorn --access-logfile - --log-level debug --workers 3 --bind 0.0.0.0:80 config.wsgi:application
