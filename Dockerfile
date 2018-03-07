FROM python:3
EXPOSE 8000
RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements.txt 
ENTRYPOINT ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
