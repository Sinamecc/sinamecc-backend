Pre-Requirements:
=================
- python3.6+ installed
- python-pip

Virtual Environment Creation:
=============================
On a working directory (for example /home/dev/sinamecc):
- `python3 -m venv env_p3`
- `source env_p3/bin/activate`
- `pip install -r requirements.txt`

Server Execution:
=================
- `python manage.py migrate` to sync database changes
- `python manage.py  createsuperuser --username admin --email "admin@foo.com"` this will be used on SINAMECC_PASSWORD variable 
- `python manage.py runserver` to run a server on http://localhost:8000

Example Requests:
=================
You need to have two environment variable:
```
export SINAMECC_USERNAME=admin
export SINAMECC_PASSWORD=YOUR_PASSWORD
```

Example to get the authenthication token:
`curl -X POST -H "Content-Type: application/json" -d "{\"username\":\"$SINAMECC_USERNAME\",\"password\":\"$SINAMECC_PASSWORD\"}" http://localhost:8000/api/v1/token/`
`
Example to get the list of `report_file` resources
`curl -X GET -H"Authorization: $(./get_token)" http://localhost:8000/api/v1/report_file/`

