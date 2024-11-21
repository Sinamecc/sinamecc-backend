FROM python:3.10

ARG FRONTEND_URL=http://localhost:3000

ARG ENV=development

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY requirements.txt /code/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code/

EXPOSE 80

STOPSIGNAL SIGTERM

ENV FRONTEND_URL=$FRONTEND_URL

CMD if [ "$ENV" = "development" ] ; then \
        echo "Running Development Server" \
    else \
        exec gunicorn --access-logfile - --log-level debug --workers 3 --bind 0.0.0.0:80 config.wsgi:application \
    fi
