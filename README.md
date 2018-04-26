Pre-Requirements:
=================
- python3.6+ installed
- python-pip

Virtual Environment Creation:
=============================
On a working directory (for example /home/dev/sinamecc-backend):
- `cd .. && python3 -m venv env_p3 && cd -`
- `source ../env_p3/bin/activate`
- `pip install -r requirements.txt`

Assumptions:
============
- Working postgresql in local environment, otherwise use `local_sqlite3` settings.
- Updated codebase (`git pull origin master`)
- Active virtualenv (PREVIOUS STEP!)

Automatic Server Setup and Execution:
=====================================
Assuming that you are in the base directory of the project (the same where you are reading this README file), execute:
- `./createsuperuser.sh`
- `./runme.sh`
- `./test-running-backend.sh`, you should see something like:
```
{"id":2,"username":"admin","email":"admin@example.com","is_active":true}
```

(OPTIONAL) Manual Server Execution:
===================================
Choose a setting file to use, for example if we want to use `local_sqlite` settings we need to execute `export DJANGO_SETTINGS_MODULE=config.settings.local_sqlite`.
The currently supported settings are: `local` (local postgres instance), `local_docker` (for docker container) and `local_sqlite` (with sqlite3 support instead of postgresql)

- `python manage.py migrate` to sync database changes
- `python manage.py  createsuperuser --username admin --email "admin@foo.com"` this will be used on SINAMECC_PASSWORD variable 
- `python manage.py runserver` to run a server on http://localhost:8000


(OPTIONAL) Example Requests:
============================

Example to get the authenthication token:
=========================================
You will need to have two environment variable:
```
export SINAMECC_USERNAME=admin
export SINAMECC_PASSWORD=cambiame
```

`curl -X POST -H "Content-Type: application/json" -d "{\"username\":\"$SINAMECC_USERNAME\",\"password\":\"$SINAMECC_PASSWORD\"}" http://localhost:8000/api/v1/token/`

Example to get the list of `report_file` resources
==================================================
You will need to have two environment variable:
```
export SINAMECC_USERNAME=admin
export SINAMECC_PASSWORD=cambiame
```

`curl -X GET -H"Authorization: $(./get_token)" http://localhost:8000/api/v1/report_file/`

(OPTIONAL) Docker:
==================
- `docker-compose build` to build an new images set
- `docker-compose up` to run the stack
- `docker-compose stop` to stop the stack
- To attach a bash you need to get the ContainerId running `docker ps`, and for example if the id was `3a87143669e4` execute `docker exec -i -t 3a87143669e4 /bin/bash`
