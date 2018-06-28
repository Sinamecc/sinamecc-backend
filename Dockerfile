FROM python:3
EXPOSE 8000
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt 
ARG setting_file=config.settings.local_sqlite
ENV DJANGO_SETTINGS_MODULE $setting_file
ENTRYPOINT ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
