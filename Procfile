release: python manage.py migrate & python manage.py curl_heroes & python manage.py import_heroes
web: gunicorn config.wsgi:application

