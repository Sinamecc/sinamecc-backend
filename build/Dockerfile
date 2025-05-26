FROM python:3.10

ARG FRONTEND_URL=http://localhost:3000

ARG ENVIRONMENT=development

ENV PYTHONUNBUFFERED=1

# Use the system Python environment and not the virtual environment (normally uv creates a virtual environment)
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

RUN mkdir /code

WORKDIR /code

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"

COPY . /code/

RUN uv sync 

EXPOSE 80

STOPSIGNAL SIGTERM

ENV FRONTEND_URL=$FRONTEND_URL
ENV ENVIRONMENT=$ENVIRONMENT

CMD ["gunicorn", "--access-logfile", "-", "--log-level", "debug", "--workers", "3", "--bind", "0.0.0.0:80", "config.wsgi:application"]
