web: gunicorn orizaba.wsgi
release: python manage.py migrate
worker: python manage.py qcluster
web: gunicorn -w 3 orizaba.wsgi --log-file -