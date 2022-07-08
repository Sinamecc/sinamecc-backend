from django.apps import apps 
from django.db import connection
cursor = connection.cursor()
cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type != 'VIEW' AND table_name NOT LIKE 'pg_ts_%%'""")
rows = cursor.fetchall()

for row in rows:
    if row[0].startswith('adaptation_action'):
        cursor.execute("DROP TABLE IF EXISTS %s CASCADE" % row[0])
        print("Delete table %s" % row[0])

cursor.execute("DELETE FROM django_migrations WHERE  app='adaptation_action';")
print("Delete record migrations in table django_migrations")
