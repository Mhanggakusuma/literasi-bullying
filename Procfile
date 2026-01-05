web: python manage.py migrate && python manage.py create_admin && gunicorn literasi_bullying.wsgi:application --bind 0.0.0.0:$PORT --timeout 120
