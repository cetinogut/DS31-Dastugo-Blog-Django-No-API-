release: python manage.py makemigrations --no-input
release: python manage.py migrate --run-syncdb

web: gunicorn dastugo_blog_proj.wsgi