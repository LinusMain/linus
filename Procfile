release: python manage.py migrate
release: python manage.py import_heroes heroes_parsed.txt
web: gunicorn config.wsgi:application

