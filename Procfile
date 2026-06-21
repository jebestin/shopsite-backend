release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
web: gunicorn shop_project.wsgi --log-file -