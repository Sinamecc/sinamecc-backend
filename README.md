# SINAMECC - National Climate Change System

SINAMECC is Costa Rica’s National Climate Change System.

## Prerequisites

- Docker >= 20.10
- Docker Compose >= 1.29

**Optional IDE support:**
- Python 3.10+
- virtualenv

## Installation and Running

1. Clone this repository:
   ```bash
   git clone https://github.com/your-org/sinamecc-backend.git
   cd sinamecc-backend
   ```

2. (Optional) Create and activate a virtual environment for local development:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # zsh
   pip install -r requirements.txt
   ```

3. Start the application using Docker Compose:
   ```bash
   docker compose up -d --build
   ```

4. Verify that containers are running:
   ```bash
   docker compose ps
   ```

## Makefile

The project includes a `Makefile` with handy commands:

```makefile
$ make help
    make re-build: Rebuild the docker image
    make up: Start the docker container
    make down: Stop the docker container
    make test: Run the tests
    make help: Show this message
    make createsuperuser: Create a superuser
    make migrate: Run the migrations
    make makemigrations: Create the migrations
```

## Advanced Usage with Docker Compose

Run Django commands for a specific module inside the `backend` container (needs to be running):

```bash
# Run the backend container
docker compose up -d 

# In another terminal, run the following commands:
# Migrate a specific module (e.g., adaptation_action)
docker compose exec backend python manage.py migrate adaptation_action
 
# Create a new superuser inside the container
docker compose exec backend python manage.py createsuperuser
```

## Default Superuser

On startup, the system creates a default superuser:

- Username: `administrator`
- Password: `cambiame`

To change this account or create additional users:
```bash
docker compose exec backend python manage.py createsuperuser
```

## Contributing

Please read the contribution guide in [GIT_GUIDELINE.md](./GIT_GUIDELINE.md).

### Pull Request Title Format

Use the following format for PR titles:
```
[issue-number] <action>: <message>
```

## License

This project is licensed under the terms in the `LICENSE` file.


## OpenAPI Documentation
The OpenAPI documentation is available at the file:
```
docs/api/openapi.yaml
<<<<<<< HEAD
```
=======
```
>>>>>>> 17a3a3a (feat: add readme)
