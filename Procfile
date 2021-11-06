release: python manage.py makemigrations --no-input
release: python manage.py migrate --run-syncdb


web: gunicorn main.wsgi