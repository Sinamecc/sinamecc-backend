.DEFAULT_GOAL := up

re-build:
	docker compose build

up:
	docker compose up backend --no-log-prefix

down:
	docker compose down

test:
	docker compose up backend -d && \
	docker compose exec backend python pytest -v -s && \
	docker compose down
createsuperuser:
	docker compose up backend -d && \
    cat ./scripts/createsuperuser.sh | docker compose exec -T backend bash && \
    docker compose down
migrate:
	docker compose up backend -d && \
	docker compose exec backend python manage.py migrate && \
	docker compose down

makemigrations:
	docker compose up backend -d && \
	docker compose exec backend python manage.py makemigrations && \
	docker compose down



help:
	@echo "    make re-build: Rebuild the docker image"
	@echo "    make up: Start the docker container"
	@echo "    make down: Stop the docker container"
	@echo "    make test: Run the tests"
	@echo "    make help: Show this message"
	@echo "    make createsuperuser: Create a superuser"
	@echo "    make migrate: Run the migrations"
	@echo "    make makemigrations: Create the migrations"