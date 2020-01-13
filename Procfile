web: gunicorn akv.wsgi --log-file -
web2: daphne akv.routing:application --port $PORT --bind 0.0.0.0 -v2 