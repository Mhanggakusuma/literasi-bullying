web: python manage.py migrate && python manage.py createsuperuser --noinput || true && gunicorn literasi_bullying.wsgi:application --bind 0.0.0.0:$PORT
