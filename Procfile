web: gunicorn config.wsgi --workers 2 --threads 4 --worker-class gthread --log-file -
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
